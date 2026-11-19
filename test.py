from src.core.exceptions import MyException
from src.core.logging import logger
import sys
a=2
try:
    logger.info("started deividing by zero")
    print(a/0)
    
except Exception as e:
    raise MyException(e,sys) from e
