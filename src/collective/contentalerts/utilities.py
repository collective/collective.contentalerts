# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWords
from plone import api

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
        if not text or text is None:
            return False

        normalized_stop_words = self.get_normalized_stop_words(stop_words)
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

    def _get_registry_stop_words(self):
        """Returns the stop words found on the registry, if any."""
        try:
            stop_words = api.portal.get_registry_record(
                name='stop_words',
                interface=IStopWords
            )
            return stop_words or None
        except KeyError:
            return None

    def get_normalized_stop_words(self, stop_words=None):
        if stop_words is None:
            stop_words = self._get_registry_stop_words()

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
