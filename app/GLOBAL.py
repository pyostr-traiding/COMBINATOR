from datetime import datetime, timedelta, UTC



class TradeStatusManager:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_already_initialized", False):
            return

        self._initialized: bool = False

        #-------------------------------------
        # Глобальная блокировка торгов
        self.STATUS_GLOBAL_BAN: int | None = 0
        self.TIMEOUT_BAN: datetime | None = None

        self._already_initialized = True

    def set_timeout_ban(self):
        """
        Устанавливает TIMEOUT_BAN на текущее время + SYMBOL_POSITION_BAN_TIME (в секундах).
        """


        self.TIMEOUT_BAN = datetime.now(UTC) + timedelta(seconds=30)

    def can_open_position(self) -> bool:
        """
        Проверяет, можно ли открывать позицию:
        - нет глобального бана
        - нет символного бана
        - не истёк TIMEOUT_BAN
        """
        now = datetime.now(UTC)

        if self.STATUS_GLOBAL_BAN:
            return False
        if self.TIMEOUT_BAN and now < self.TIMEOUT_BAN:
            return False

        return True

TRADE_STATUS_MANAGER = TradeStatusManager()