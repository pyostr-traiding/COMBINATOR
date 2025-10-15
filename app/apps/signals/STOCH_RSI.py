import datetime

from klines.utils import ms_to_dt

from app.TARGETS import TargetsIndicator, TargetValues
from app.callbacks.schema.stochRSI import PredictStochRSISchema


def update_stoch_rsi(data: PredictStochRSISchema):
    """
    Обновляем target‑значения стохастика RSI по всем пришедшим интервалам.
    """
    for val in data.values:
        dt = ms_to_dt(val.kline_ms)
        TargetsIndicator.STOCH_RSI[val.interval] = TargetValues(
            side=val.side,
            target_rate=val.target_rate,
            kline_dt=dt,
            create_dt=datetime.datetime.now(datetime.UTC),
            interval=val.interval,
            kline_ms=val.kline_ms,
        )
