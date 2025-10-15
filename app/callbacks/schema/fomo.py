from pydantic import BaseModel


class FOMOSchema(BaseModel):
    """
    Схема сигнала FOMO индикатора
    """
    indicator: str
    symbol: str
    type: str
    interval: int
    timestamp: int
    ma: float
    fomo_up: float
    fomo_down: float
    fomo_percent: float
