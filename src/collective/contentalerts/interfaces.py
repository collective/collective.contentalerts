# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from collective.contentalerts import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveContentalertsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IStopWords(Interface):

    stop_words = schema.Text(
        title=_(
            u'settings_stop_words_list_title',
            default=u'List'
        ),
        description=_(
            u'settings_stop_words_list_description',
            default=u'Words/sentences that will generate an alert, '
                    u'one per line.'
        ),
        required=False,
    )
