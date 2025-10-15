import os

import aiohttp
import requests
from dotenv import load_dotenv


load_dotenv()

def create_position(
    symbol: str,
    uuid: str,
    side: str,
    qty: str,
    price: str,
    kline_ms: str,
    orderType: str = 'Limit',
    category: str = 'spot',
    takeProfit: str = None,
    stopLoss: str = None,
    is_test: bool = True,
):
    """

    """
    base_url = os.getenv('BASE_API_URL')
    url = f'{base_url}/position/createPosition'
    params = {
      "symbol_name": symbol,
      "uuid": uuid,
      "category": category,
      "side": side,
      "orderType": orderType,
      "qty": qty,
      "price": price,
      "takeProfit": takeProfit,
      "stopLoss": stopLoss,
      "kline_ms": kline_ms,
      "is_test": is_test
    }
    res = requests.post(
        url=url,
        params=params,
        headers={'Content-Type': 'application/json'},
        json=params
    )
    if res.status_code in [200, 409]:
        return True
    return False

#
# create_position(
#     symbol='BTCUSDT',
#     uuid='3920jfs',
#     side='sell',
#     qty='0.22',
#     price='112022',
#     kline_ms='23124231',
# )