# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

import pkg_resources


try:
    pkg_resources.get_distribution('collective.taskqueue')
except pkg_resources.DistributionNotFound:
    ASYNC = False
else:
    ASYNC = True

_ = MessageFactory('collective.contentalerts')
