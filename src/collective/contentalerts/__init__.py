# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

import logging
import pkg_resources


try:
    pkg_resources.get_distribution('collective.taskqueue')
except pkg_resources.DistributionNotFound:
    ASYNC = False
else:
    ASYNC = True


PACKAGE_NAME = 'collective.contentalerts'

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
