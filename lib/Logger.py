
import logging
import os
import traceback

class Logger():

    def __set_logger(self, client, log_directory):
        # log_directory = config_environment('LOG_DIRECTORY')
        log_filename = f'{client}.log'

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger

    @classmethod
    def add_to_log(self, level, message, log_directory, client='log'):
        try:
            logger = self.__set_logger(self, client, log_directory)

            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
            elif (level == "success"):
                logger.info(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)