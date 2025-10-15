"""
Целевые значения по индикаторам

Данные отслеживаются для всех интервалов

Искать необходимо точки входа
Для продажи:
- RSI > 70
- Stoch RSI > 90 | 90
- FOMO - Приближение к верхней границе
- Изменение объёма (выяснить как)

Для покупки:
- RSI < 30
- Stoch RSI > 10 | 10
- FOMO - Приближение к нижней границе
- Изменение объёма (выяснить как)

Есть задача состоящая из вопроса как вести данные с нескольких интервалов
Необходимо учесть, что точка входа по RSI смотрится не только по минутному интервалу,
но и по старшим графикам:
1м - 90
5м - 80
15м - 75
30м - 83

Нужно создать массивы содержащие все интервалы для каждого из индикаторов
В панели есть конфигурация которая укажет какие интервалы учитывать в данный момент

Так же конфигурация содержит целевые диапазоны, по постижению которых можно открыть позицию

"""
from datetime import datetime
from typing import Dict, ClassVar, Optional

from pydantic import BaseModel

RSI: float = 100_500.00
STOCH_RSI: float = 100_100.00
FOMO: float = 100_100.00


class TargetValues(BaseModel):
    side: str
    target_rate: Optional[float] = None
    kline_dt: datetime
    create_dt: datetime
    interval: int
    kline_ms: int


class TargetsIndicator(BaseModel):
    RSI: ClassVar[Dict[int, TargetValues]] = {}
    STOCH_RSI: ClassVar[Dict[int, TargetValues]] = {}
    FOMO: ClassVar[Dict[int, TargetValues]] = {}
