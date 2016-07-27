# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.textfield.interfaces import IRichTextValue
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import HTMLParser
import re
import unicodedata


NBSP_RE = re.compile(r'\s+|&#160;|&nbsp;', re.UNICODE)


class Alert(object):
    """Utility to know if a given text contains stop words."""

    def get_snippets(self, text, stop_words=None, chars=150):
        """Returns the stop words found in the text.

        See IAlert interface docstring for its parameters.
        """
        if text is None:
            return u''

        normalized_stop_words = self.get_normalized_stop_words(stop_words)
        if not normalized_stop_words:
            return u''

        # get all the stop words occurrences on the text
        snippets_data = {}
        normalized_text = alert_text_normalize(text)
        for word in normalized_stop_words:
            index = normalized_text.find(word)
            while index != -1:
                snippet = self._snippet(
                    normalized_text,
                    index,
                    word,
                    chars
                )
                snippets_data[index] = (snippet, word)

                index = normalized_text.find(word, index + 1)

        if not snippets_data:
            return u''

        # sort the snippets so that the original text flow is respected
        snippet = u''
        stop_words_found = []
        for index in sorted(snippets_data.keys()):
            snippet += snippets_data[index][0]
            stop_words_found.append(snippets_data[index][1])

        result = u'{0}{1}'.format(
            ', '.join(self._unique(stop_words_found)),
            snippet
        )
        return result

    def has_stop_words(self, text, stop_words=None):
        """Checks if the given text has words from the provided stop words.

        See IAlert interface docstring for its parameters.
        """
        return self._has_words(text, stop_words=stop_words)

    def has_forbidden_words(self, text):
        """Checks if the given text has words from the forbidden stop words
        list

        See IAlert interface docstring for its parameters.
        """
        return self._has_words(text, register='forbidden_words')

    def has_inadequate_words(self, text):
        """Checks if the given text has words from the inadequate stop words
        list

        See IAlert interface docstring for its parameters.
        """
        return self._has_words(text, register='inadequate_words')

    def _has_words(self, text, stop_words=None, register=None):
        if not text:
            return False

        normalized_stop_words = self.get_normalized_stop_words(
            stop_words=stop_words,
            register=register,
        )
        if not normalized_stop_words:
            return False

        normalized_text = alert_text_normalize(text)
        for word in normalized_stop_words:
            if normalized_text.find(word) != -1:
                return True

        return False

    @staticmethod
    def _snippet(text, index, word, chars):
        """Get the surrounding text of the given word in the given text.

        :param text: the text where the word is found.
        :type text: unicode
        :param index: position where the word is found within the text.
        :type index: int
        :param word: the word that is found on the text.
        :type word: unicode
        :param chars: the amount of surrounding text.
        :type chars: int
        :returns: the word with extra characters before and after it.
        :rtype: unicode
        """
        before = index - chars
        if before < 0:
            before = 0
        after = index + len(word) + chars
        return u'\n\n...{0}...'.format(text[before:after])

    @staticmethod
    def _unique(sequence):
        """Remove duplicates from the sequence keeping the sorting order.

        :param sequence: the iterable which has duplicates on its elements.
        :type sequence: iterable
        :returns: the same list as provided with the duplicates removed.
        :rtype: list
        """
        seen = set()
        seen_add = seen.add
        return [x for x in sequence if not (x in seen or seen_add(x))]

    def _get_registry_stop_words(self, register=None):
        """Returns the stop words found on the registry, if any."""
        return_stop_words = ''

        if register is None:
            register = ('forbidden_words', 'inadequate_words', )
        elif isinstance(register, str):
            register = (register, )

        for key_name in register:
            try:
                stop_words = api.portal.get_registry_record(
                    name=key_name,
                    interface=IStopWords
                )
                if stop_words:
                    return_stop_words += u'\n{0}'.format(stop_words)
            except (KeyError, InvalidParameterError):
                pass

        return return_stop_words

    def get_normalized_stop_words(self, stop_words=None, register=None):
        if stop_words is None:
            stop_words = self._get_registry_stop_words(register=register)

        if stop_words is None or stop_words.strip() == u'':
            return []

        normalized_stop_words = [
            alert_text_normalize(a)
            for a in stop_words.splitlines()
            if a
        ]
        return normalized_stop_words


def alert_text_normalize(text):
    """Transform text in a way that is suitable for string comparison.

    :param text: text that will be transformed.
    :type text: str or unicode
    :returns: text normalized.
    :rtype: unicode
    """
    if IRichTextValue.providedBy(text):
        text = text.raw
    if isinstance(text, str):
        text = text.decode('latin-1')
    text = NBSP_RE.sub(' ', text)
    parser = HTMLParser.HTMLParser()
    text = parser.unescape(text)
    text = text.lower()
    text = u''.join(
        [c
         for c in unicodedata.normalize('NFKD', text)
         if not unicodedata.combining(c)]
    )

    return text


def get_text_from_object(obj):
    """Get the text from an object.

    The object can be a comment, a Dexterity object or an event holding any
    of the two.
    """
    text = u''

    if getattr(obj, 'text', None):
        text = obj.text

    # if it's an event on a comment
    elif getattr(obj, 'comment', None) and \
            getattr(obj.comment, 'text', None):
        text = obj.comment.text

    # if it's an event on a DX type
    elif getattr(obj, 'object', None):
        obj = obj.object
        if getattr(obj, 'text', None):
            text = obj.text

    return text


def get_new_entries(old_entries, new_entries):
    """Return the newly added entries between two lists

    New lines are discarded and the order does not matter.

    Returns a list of all new element were added.
    """
    if new_entries is None:
        return []

    old_set = set([])
    if old_entries:
        old_set = set([
            alert_text_normalize(e)
            for e in old_entries.split('\n')
        ])
        old_set -= {u'', }  # remove empty string

    new_set = set([
        alert_text_normalize(e)
        for e in new_entries.split('\n')
    ])
    new_set -= {u'', }  # remove empty string

    # set difference, see:
    # https://docs.python.org/2/library/stdtypes.html#set.difference
    return sorted(list(new_set - old_set))


def verify_brain(brain, new_entries):
    """Check if the given brain's text has the given new entries

    If so, switch the marker interfaces.
    """
    try:
        obj = brain.getObject()
    except AttributeError:
        # it's not a brain, but something else, so abort silently
        return
    text = get_text_from_object(obj)
    utility = getUtility(IAlert)
    if utility.has_stop_words(text, stop_words=new_entries):
        noLongerProvides(obj, IStopWordsVerified)
        alsoProvides(obj, IHasStopWords)
        obj.reindexObject(idxs=('object_provides', ))
