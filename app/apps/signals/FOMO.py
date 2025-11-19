import datetime

from app.TARGETS import TargetsIndicator, TargetValues
from app.callbacks.schema.fomo import FOMOSchema
from klines.utils import ms_to_dt


def update_fomo(data: FOMOSchema):
    """
    Обновляем target‑значения FOMO по всем пришедшим интервалам.
    """
    side = 'sell' if data.ma > data.fomo_up else 'buy'

    TargetsIndicator.FOMO[data.interval] = TargetValues(
        side=side,
        target_rate=None,
        kline_dt=ms_to_dt(data.timestamp),
        create_dt=datetime.datetime.now(datetime.UTC),
        interval=data.interval,
        kline_ms=data.timestamp,
    )
