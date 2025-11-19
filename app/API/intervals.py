import json
import os

from cachetools import TTLCache, cached

from conf.conf_redis import redis_settings

rsi_cache = TTLCache(maxsize=100, ttl=5)

@cached(cache=rsi_cache)
def get_intervals() -> dict:
    """
    Загружает интервалы и приводит ключи к int.
    """
    data = redis_settings.get('settings:indicator:INTERVALS')
    if not data:
        return {}

    data = json.loads(data)

    # преобразование строковых ключей в int
    data = {int(k): v for k, v in data.items()}

    return data
