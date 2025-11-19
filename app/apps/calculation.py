import ast
import time

from datetime import datetime, timezone
from uuid import uuid4

from app.API.intervals import get_intervals
from app.API.positions import create_position
from app.GLOBAL import TRADE_STATUS_MANAGER
from app.TARGETS import TargetsIndicator
from conf.settings import settings

last_update: float = 0
UPDATE_INTERVAL = 30  # секунд


def all_equal(lst):
    return len(set(lst)) == 1 if lst else False


def check_candles_timestamps(candle_data):
    """
    Проверяет, соответствует ли каждая переданная свеча текущему времени.

    Вход:
        candle_data: список [ [интервал_в_минутах, таймстемп_в_мс], ... ]

    Возвращает:
        словарь {интервал: True/False}
    """
    now_dt = datetime.fromtimestamp(time.time(), timezone.utc)
    result = {}

    for interval, ts_ms in candle_data:
        candle_time = datetime.fromtimestamp(ts_ms / 1000, timezone.utc)

        if interval < 60:
            expected_minutes = (now_dt.minute // interval) * interval
            expected_dt = now_dt.replace(minute=expected_minutes, second=0, microsecond=0)
        else:
            expected_hours = (now_dt.hour // (interval // 60)) * (interval // 60)
            expected_dt = now_dt.replace(hour=expected_hours, minute=0, second=0, microsecond=0)

        expected_ts_ms = int(expected_dt.timestamp() * 1000)
        result[interval] = ts_ms == expected_ts_ms

    return result



def calculation_position():
    global last_update
    """
    Получаем с панели включенные интервалы

    Проверяем что все включенные в панели интервалы в TargetsIndicator имеют данные

    Проверяем что все значения TargetsIndicator принадлежат одному диапазону времени,
    что бы избежать устаревших данных

    Проверяем что все включенные интервалы указывают на одну и туже сторону (buy|sell)
    Если все проверки прошли:
      Берем все значения TargetsIndicator и на их основе делаем расчет
      RSI - считаем среднее значение target_rate
      ADX - сила есть
      MACD - направление тренда совпадает с side RSI
      FOMO - находимся близко к границам
    """
    intervals: dict[int, bool] = get_intervals()

    # Обновляем раз в UPDATE_INTERVAL секунд данные по интервалам
    if not intervals:
        if settings.DEBUG_PRINT:
            print('нет интервалов')
        return

    RSI = TargetsIndicator.RSI
    STOCH_RSI = TargetsIndicator.RSI
    FOMO = TargetsIndicator.FOMO
    if not RSI:
        if settings.DEBUG_PRINT:
            print('Нет данных RSI')
        return

    if not STOCH_RSI:
        if settings.DEBUG_PRINT:
            print('Нет данных STOCH RSI')
        return

    """
    Проверяем что все включенные интервалы есть в индикаторе 
    """
    for key, value in intervals.items():
        key = int(key)
        if value and key not in RSI:
            if settings.DEBUG_PRINT:
                print(f'В RSI нет ключа {key} {value} {RSI}')
            return

        if value and key not in STOCH_RSI:
            if settings.DEBUG_PRINT:
                print(f'В STOCH_RSI нет ключа {key} {value} {STOCH_RSI}')
            return

    """
    Сверяемся что индикаторы все индикаторы показывают sell или buy
    """
    if not all_equal([value.side for key, value in RSI.items()]): return
    if not all_equal([value.side for key, value in STOCH_RSI.items()]): return

    """
    Проверяем что все свечи имеют одну временную метку и не устарели 
    """
    rsi_candles_timestamp = [[value.interval, value.kline_ms] for key, value in RSI.items()]
    stoch_rsi_candles_timestamp = [[value.interval, value.kline_ms] for key, value in STOCH_RSI.items()]

    # Если хотя бы один таймфрейм не входит в нужное значение
    if not all(check_candles_timestamps(rsi_candles_timestamp).values()):
        if settings.DEBUG_PRINT:
            print('RSI не готов')
        return

    if not all(check_candles_timestamps(stoch_rsi_candles_timestamp).values()):
        if settings.DEBUG_PRINT:
            print('Stoch RSI не готов')
        return

    """
    Вычисляем цену для входа на основе средней цены RSI и STOCH RSI
    """

    target_rates = [value.target_rate for key, value in RSI.items()] + [value.target_rate for key, value in STOCH_RSI.items()]
    target_rate = float(sum(target_rates) / len(target_rates))
    first_key = next(iter(RSI))
    first_value = RSI[first_key]
    side = first_value.side
    symbol = 'BTCUSDT'
    uuid = str(uuid4())

    create_position(
        symbol=symbol,
        side=side,
        uuid=uuid,
        price=str(target_rate),
        kline_ms=str(RSI[1].kline_ms)
    )

    text = (
        '--------------\n'
        f'ID: {uuid}\n\n'
        f'Сторона: {side}\n'
        f'Символ: {symbol}\n'
        f'Цена: {target_rate}\n'
        f'Кол-во: 0.001\n'
    )


    # send_to_rabbitmq(
    #     {
    #         "is_test": True,
    #         "notification": False,
    #         "text": text
    #     }
    # )
    TRADE_STATUS_MANAGER.set_timeout_ban()
