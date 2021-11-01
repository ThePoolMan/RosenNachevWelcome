import logging
from loguru import logger

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
logger.add("INFO.log", format="{time} {level} {message}", level="INFO", rotation="1000 KB", compression="zip")
