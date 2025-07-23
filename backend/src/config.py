import sys

from dotenv import dotenv_values
from loguru import logger

logger.remove()

# DEBUG и выше — в консоль
logger.add(sys.stderr, level="DEBUG", format="{time} | {level} | {message}")

# Только INFO и выше — в файл
logger.add(
    "logs/app.log",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    format="{time} | {level} | {message}",
)


main_config = dotenv_values(".env")

config = dotenv_values(f".env.{main_config.get('ENV', 'prod')}")