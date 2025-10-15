import datetime

from app.TARGETS import TargetsIndicator, TargetValues
from app.callbacks.schema.rsi import PredictRSISchema
from klines.utils import ms_to_dt


def update_rsi(data: PredictRSISchema):
    """
    Обновляем target‑значения RSI по всем пришедшим интервалам.
    """
    for val in data.values:
        dt = ms_to_dt(val.kline_ms)
        TargetsIndicator.RSI[val.interval] = TargetValues(
            side=val.side,
            target_rate=val.target_rate,
            kline_dt=dt,
            create_dt=datetime.datetime.now(datetime.UTC),
            interval=val.interval,
            kline_ms=val.kline_ms,
        )
