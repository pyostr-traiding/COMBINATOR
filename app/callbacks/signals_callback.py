import json

from app.GLOBAL import TRADE_STATUS_MANAGER
from app.apps.calculation import calculation_position
from app.apps.signals.FOMO import update_fomo
from app.apps.signals.RSI import update_rsi
from app.apps.signals.STOCH_RSI import update_stoch_rsi

from app.callbacks.schema.fomo import FOMOSchema
from app.callbacks.schema.rsi import PredictRSISchema
from app.callbacks.schema.stochRSI import PredictStochRSISchema
from conf.settings import settings


def callback_signals(
        data: str,
):
    """
    Callback для обновления настроек
    """
    data = json.loads(data)
    if not TRADE_STATUS_MANAGER.can_open_position():
        if settings.DEBUG_PRINT:
            print('Блокировка')
        return
    """
    Определяем какой это индикатор

    После обновления значения проверяем все ли индикаторы показывают одно значение
    Если да - создаем позицию
    """
    if data['type'] == 'PREDICT.RSI':
        rsi_schema = PredictRSISchema(
            **data
        )
        update_rsi(data=rsi_schema)
    elif data['type'] == 'PREDICT.STOCH_RSI':
        stoch_rsi_schema = PredictStochRSISchema(
            **data
        )
        update_stoch_rsi(data=stoch_rsi_schema)
    elif data['type'] == 'VALUE.FOMO':
        fomo_schema = FOMOSchema(
            **data
        )
        update_fomo(data=fomo_schema)

    calculation_position()