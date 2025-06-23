from loguru import logger

logger.remove()
logger.add("file_{time}.log", rotation="1 MB", enqueue=True, backtrace=True, diagnose=True)
