import time

from app.callbacks.signals_callback import callback_signals
from conf.conf_redis import redis_signals
from conf.settings import settings


print(f'Запуск комбинатора для {settings.SYMBOL}')


print('Запуск каналов')
pubsub_signals = redis_signals.pubsub()

pubsub_signals.subscribe(f'signals:{settings.SYMBOL}')


if __name__ == "__main__":
    try:
        while True:
            message_signals = pubsub_signals.get_message()

            if message_signals and not isinstance(message_signals['data'], int):
                callback_signals(message_signals['data'])


            time.sleep(0.01)  # небольшая задержка, чтобы не грузить CPU

    except KeyboardInterrupt as e:
        print(f'Закрытие: {e}')

