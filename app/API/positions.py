import os

import aiohttp
import requests
from dotenv import load_dotenv


load_dotenv()

def create_position(
    symbol: str,
    uuid: str,
    side: str,
    price: str,
    kline_ms: str,
    is_test: bool = True,
):
    """

    """
    base_url = os.getenv('BASE_API_URL')
    url = f'{base_url}/position/create'
    params = {
      "symbol_name": symbol,
      "uuid": uuid,
      "side": side,
      "price": price,
      "kline_ms": kline_ms,
      "is_test": is_test
    }
    res = requests.post(
        url=url,
        params=params,
        headers={'Content-Type': 'application/json'},
        json=params
    )
    print(res)
    if res.status_code in [200, 409]:
        return True
    return False


create_position(
    symbol='BTCUSDT',
    uuid='3920jfs',
    side='sell',
    price='112022',
    kline_ms='23124231',
)