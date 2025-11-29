import ast
import os
from pprint import pprint

from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient

load_dotenv()


# Инициализация клиента
client = InfisicalSDKClient(
    host=os.getenv('INFISICAL_HOST'),
    token=os.getenv('INFISICAL_TOKEN'),
    cache_ttl=300
)

print(os.getenv('INFISICAL_HOST'))
print(os.getenv('INFISICAL_TOKEN'))

def load_project_secrets(project_slug: str):
    resp = client.secrets.list_secrets(
        project_slug=project_slug,
        environment_slug=os.getenv('ENVIRONMENT_SLUG'),
        secret_path="/"
    )
    return {s['secretKey']: s['secretValue'] for s in resp.to_dict()['secrets']}

# Загружаем общие секреты
shared_secrets = load_project_secrets("shared-all")

# Загружаем проектные секреты
project_secrets = load_project_secrets("combinator")

# Объединяем: проектные перезаписывают общие при совпадении ключей
all_secrets = {**shared_secrets, **project_secrets}

# Добавляем в окружение
os.environ.update(all_secrets)
pprint(all_secrets)

class Settings:

    SYMBOL: str = os.getenv('SYMBOL')

    BASE_API_URL: str = os.getenv('BASE_API_URL')

    DEBUG_PRINT: bool = ast.literal_eval(os.getenv('DEBUG_PRINT'))

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT'))
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')

    RABBITMQ_USERNAME: str = os.getenv('RABBITMQ_USERNAME')
    RABBITMQ_PASSWORD: str = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT: str = int(os.getenv('RABBITMQ_PORT'))
    RABBITMQ_VIRTUAL_HOST: str = os.getenv('RABBITMQ_VIRTUAL_HOST')

    INFISICAL_HOST: str = os.getenv('INFISICAL_HOST')
    INFISICAL_TOKEN: str = os.getenv('INFISICAL_TOKEN')

settings = Settings()
