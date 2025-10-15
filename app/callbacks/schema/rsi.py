from typing import List

from pydantic import BaseModel


class PredictRSIValueSchema(BaseModel):

    kline_ms: int
    interval: int
    value: float
    side: str
    percent: float
    target_rate: float


class PredictRSISchema(BaseModel):
    """
    Схема RSI
    """
    kline_ms: int
    symbol: str
    type: str
    values: List[PredictRSIValueSchema]
