import ast
import os

from dotenv import load_dotenv

load_dotenv()

class Settings:

    SYMBOL: str = 'BTCUSDT'

    DEBUG_PRINT: bool = ast.literal_eval(os.getenv('DEBUG_PRINT'))

settings = Settings()
