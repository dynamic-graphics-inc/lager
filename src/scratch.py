# import lager
from lager import logger
import inspect

members = inspect.getmembers(logger)

logger.info("a message")
logger + "herm"
logger += "asdf"
print(logger)

logger + "some string"
print(logger)
def thing():
    logger + "ohno"
    print(logger)
    logger + "ohno"
    print(logger)
    # logger += "another"


thing()
