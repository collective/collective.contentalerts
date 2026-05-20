from importlib.metadata import distribution
from importlib.metadata import PackageNotFoundError
from zope.i18nmessageid import MessageFactory

import logging

try:
    distribution("collective.taskqueue")
except PackageNotFoundError:
    ASYNC = False
else:
    ASYNC = True


PACKAGE_NAME = "collective.contentalerts"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
