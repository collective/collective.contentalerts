# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from collective.contentalerts import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveContentalertsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IStopWords(Interface):
    """Registry settings schema being used by this distribution."""

    forbidden_words = schema.Text(
        title=_(
            u'settings_forbidden_words_list_title',
            default=u'Forbidden words'
        ),
        description=_(
            u'settings_forbidden_words_list_description',
            default=u'Words/sentences that will prevent an object to be made '
                    u'public, one per line.'
        ),
        required=False,
    )

    inadequate_words = schema.Text(
        title=_(
            u'settings_inadequate_words_list_title',
            default=u'List'
        ),
        description=_(
            u'settings_inadequate_words_list_description',
            default=u'Words/sentences that will generate an alert, '
                    u'one per line.'
        ),
        required=False,
    )


class IAlert(Interface):
    """Utility to know if a given text contains stop words."""

    def get_snippets(text, stop_words=None, chars=150):
        """Returns the stop words found in the text surrounded by some text.

        :param text: where stop words will be searched on.
        :type text: str
        :param chars: how many surrounding characters should be shown around
            a stop word.
        :type chars: int
        :param stop_words: list of words that will be searched on the text.
            If not provided the default.
        :type stop_words: list
        :returns: formatted text with a list of the stop words found and the
          snippets below them.
        :rtype: str
        """

    def has_stop_words(text, stop_words=None):
        """Checks if the given text has words from the provided stop words.

        :param text: where stop words will be searched on.
        :type text: str
        :param stop_words: list of words that will be searched on the text.
        :type stop_words: list
        :returns: whether the text contains words from the stop words.
        :rtype: bool
        """

    def has_forbidden_words(text):
        """Checks if the given text has words from the forbidden stop words
        list

        :param text: where forbidden words will be searched on.
        :type text: str
        :returns: whether the text contains forbidden words.
        :rtype: bool
        """

    def has_inadequate_words(text):
        """Checks if the given text has words from the inadequate stop words
        list

        :param text: where inadequate words will be searched on.
        :type text: str
        :returns: whether the text contains forbidden words.
        :rtype: bool
        """


class ITextAlertCondition(Interface):
    """Schema for the text alert plone.app.contentrules condition."""

    stop_words = schema.Text(
        title=_(
            u'contentrules_text_alert_condition_field_title',
            default=u'Stop words'
        ),
        description=_(
            u'contentrules_text_alert_condition_field_description',
            default=u'One stop word per line, keep it empty if you want to '
                    u'use the generic one.'
        ),
        required=False,
    )


class IInadequateTextAlertCondition(ITextAlertCondition):
    pass


class IForbiddenTextAlertCondition(ITextAlertCondition):
    pass


class IHasStopWords(Interface):
    """Marker interface attached to objects that have stop words."""


class IStopWordsVerified(Interface):
    """Marker interface attached to objects that do have stop words but that
    they have been verified and approved
    """
