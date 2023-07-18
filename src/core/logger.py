import logging
from datetime import datetime
from sqlalchemy.orm import Session
from database.models import models
from database.database import get_db

class AccumulatingLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_entries = []

    def emit(self, record):
        message = self.format(record)
        self.log_entries.append(message)


class LoggerHandler:
    def __init__(self, db: Session):
        self.__session = next(db)
        self.__bot_log = None
        self.start_time = datetime.now()
        self.errors = 0
        self.warnings = 0

        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)

        self.log_handler = AccumulatingLogHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

        # Adiciona o StreamHandler para exibir o log no console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.info(f"[LOG] StartTime: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
        self.warnings += 1

    def error(self, message):
        self.logger.error(message)
        self.errors += 1

    def set_bot_log(self, bot_log: models.BotLog = None):
        self.__bot_log = bot_log

        if bot_log is None:
            self.__bot_log = models.BotLog(start_at=datetime.utcnow())
    
    def set_bot_log_uptades(self, updates:str):
        self.__bot_log.updates = updates

    def save_log(self):

        log_entry = models.Logger(
            errors=self.errors,
            warnings=self.warnings,
            logger='\n'.join(self.log_handler.log_entries)
        )

        log_entry.save_and_commit(self.__session)

        return log_entry
    
    def save_bot_log(self, log_id):
        self.__bot_log.logger_id = log_id
        self.__bot_log.save_and_commit(self.__session)
    
    def close(self):
        end_time = datetime.now()
        elapsed_time = end_time - self.start_time
        self.logger.info(f"[LOG] EndTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"[LOG] ExecTime: {elapsed_time}")
        
        if self.__bot_log:
            log = self.save_log()
            bot = self.save_bot_log(log_id=log.id)

        elif self.errors > 0:
            self.save_log()

class LoggerSingleton:
    __instance = None

    @classmethod
    def get_instance(cls, db: Session):
        if cls.__instance is None:
            cls.__instance = LoggerHandler(db)
        return cls.__instance


logger = LoggerSingleton().get_instance(get_db())