from typing import List

from pydantic import BaseModel


class PredictStochRSIValueSchema(BaseModel):
    kline_ms: int
    interval: int
    value_k: float
    value_d: float
    side: str
    percent: float
    target_rate: float


class PredictStochRSISchema(BaseModel):
    """
    Схема RSI
    """
    kline_ms: int
    symbol: str
    type: str
    values: List[PredictStochRSIValueSchema]
