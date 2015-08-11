# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from collective.contentalerts.utilities import Alert
from zope.component import getUtility

import unittest


class AlertUtilityTestCase(unittest.TestCase):
    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.utility = getUtility(IAlert)

    def test_utility_exists(self):
        self.assertTrue(self.utility)


class HTMLNormalizeTestCase(unittest.TestCase):

    def setUp(self):
        self.normalize = Alert.html_normalize

    def test_regular_text_left_as_is(self):
        text = u'normal text'
        self.assertEqual(self.normalize(text), text)

    def test_lower_case(self):
        text = u'UAU'
        self.assertEqual(self.normalize(text), u'uau')

    def test_unicode_normalized_form(self):
        text = u'süspicious'
        self.assertEqual(self.normalize(text), u'suspicious')

    def test_unicode_normalized_form_lower_case(self):
        text = u'sÜspicious'
        self.assertEqual(self.normalize(text), u'suspicious')

    def test_html_entity(self):
        text = u's&#220;spicious'
        self.assertEqual(self.normalize(text), u'suspicious')

    def test_html_entity_lower_case(self):
        text = u's&#252;spicious'
        self.assertEqual(self.normalize(text), u'suspicious')

    def test_multiple_spaces_on_source(self):
        text = u'suspicious     text'
        self.assertEqual(self.normalize(text), u'suspicious text')

    def test_string(self):
        text = 'some string'
        self.assertEqual(self.normalize(text), text)

    def test_string_umlauts(self):
        text = 'some \xfc'
        self.assertEqual(self.normalize(text), u'some u')


class SnippetTestCase(unittest.TestCase):

    def setUp(self):
        self.snippet = Alert._snippet

    def test_snippet_is_returned(self):
        text = u'normal text with more '
        self.assertEqual(
            self.snippet(text, text.find('text'), 'text', 3),
            '\n\n...al text wi...'
        )

    def test_padding(self):
        text = u'normal text with more'
        self.assertEqual(
            self.snippet(text, text.find('text'), 'text', 5),
            '\n\n...rmal text with...'
        )

    def test_more_padding_than_text(self):
        text = u'normal text with more'
        self.assertEqual(
            self.snippet(text, text.find('text'), 'text', 150),
            '\n\n...normal text with more...'
        )

    def test_text_at_the_end(self):
        text = u'normal text'
        self.assertEqual(
            self.snippet(text, text.find('text'), 'text', 2),
            '\n\n...l text...'
        )

    def test_text_at_the_beginning(self):
        text = u'normal text'
        self.assertEqual(
            self.snippet(text, text.find('text'), 'text', 2),
            '\n\n...l text...'
        )


class UniqueTestCase(unittest.TestCase):

    def setUp(self):
        self.unique = Alert._unique

    def test_no_dups_same_list(self):
        elements = ('a', 'b', )
        self.assertEqual(len(self.unique(elements)), len(elements))

    def test_only_unique(self):
        elements = ('a', 'b', 'a', )
        unique = self.unique(elements)
        self.assertEqual(unique, ['a', 'b'])


class GetSnippetsTestCase(unittest.TestCase):

    def setUp(self):
        self.snippets = Alert().get_snippets

    def test_no_text(self):
        text = None
        stop_words = u'one\ntwo'
        self.assertEqual(self.snippets(text, stop_words), u'')

    def test_empty_text(self):
        text = u''
        stop_words = u'one\ntwo'
        self.assertEqual(self.snippets(text, stop_words), u'')

    def test_no_stop_word_in_text(self):
        text = u'Random normal text'
        stop_words = u'one\ntwo'
        self.assertEqual(self.snippets(text, stop_words), u'')

    def test_stop_word_in_text(self):
        text = u'Alerts two text'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=1)
        self.assertEqual(snippet_text, u'two\n\n... two ...')

    def test_unicode_text(self):
        text = u'Alerts twö text'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=3)
        self.assertEqual(snippet_text, u'two\n\n...ts two te...')

    def test_multiple_stop_words(self):
        text = u'Alerts one text and two more text'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=1)
        self.assertEqual(
            snippet_text,
            u'one, two\n\n... one ...\n\n... two ...'
        )

    def test_same_stop_word_more_than_once(self):
        text = u'Alerts one text and one more text'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=3)
        self.assertEqual(
            snippet_text,
            u'one\n\n...ts one te...\n\n...nd one mo...'
        )

    def test_keep_text_in_order(self):
        """Show the snippets in the order they appear on the text.

        In this text the stop words are 'one' and 'two' and in the text 'two'
        is the first to be show up, thus a normal iteration over the text would
        report 'one' first and then 'two', which is the other way around on the
        text.
        """
        text = u'Alerts two text and one more text'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=3)
        self.assertEqual(
            snippet_text,
            u'two, one\n\n...ts two te...\n\n...nd one mo...'
        )

    def test_keep_text_in_order_multiple_occurrences(self):
        text = u'Alerts two text and one more text and some more two tired'
        stop_words = u'one\ntwo'
        snippet_text = self.snippets(text, stop_words, chars=2)
        self.assertEqual(
            snippet_text,
            u'two, one\n\n...s two t...\n\n...d one m...\n\n...e two t...'
        )
