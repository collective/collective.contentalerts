# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from collective.contentalerts.utilities import Alert
from collective.contentalerts.utilities import alert_text_normalize
from collective.contentalerts.utilities import get_new_entries
from collective.contentalerts.utilities import get_text_from_object
from collective.contentalerts.utilities import verify_brain
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


class AlertUtilityTestCase(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.registry = getUtility(IRegistry)
        self.utility = getUtility(IAlert)

    def _set_record_value(self, value, record='inadequate_words'):
        api.portal.set_registry_record(
            name=record,
            interface=IStopWords,
            value=value
        )

    def _set_all_records(self, inadequate=u'inade', forbidden=u'forbid'):
        api.portal.set_registry_record(
            name='inadequate_words',
            interface=IStopWords,
            value=inadequate
        )
        api.portal.set_registry_record(
            name='forbidden_words',
            interface=IStopWords,
            value=forbidden
        )

    def test_utility_exists(self):
        self.assertTrue(self.utility)

    def test_no_forbidden_registry_no_error(self):
        """Check that if the forbidden registry does not exist the utility
        handles it
        """
        # delete the record on the registry
        key = IStopWords.__identifier__ + '.forbidden_words'
        del self.registry.records[key]

        self.assertEqual(
            self.utility._get_registry_stop_words(),
            ''
        )

    def test_no_inadequate_registry_no_error(self):
        """Check that if the inadequate registry does not exist the utility
        handles it
        """
        # delete the record on the registry
        key = IStopWords.__identifier__ + '.inadequate_words'
        del self.registry.records[key]

        self.assertEqual(
            self.utility._get_registry_stop_words(),
            ''
        )

    def test_no_registry_no_error(self):
        """Check that if none of the registries exist registry the utility
        handles it
        """
        # delete the records on the registry
        key = IStopWords.__identifier__ + '.inadequate_words'
        del self.registry.records[key]
        key = IStopWords.__identifier__ + '.forbidden_words'
        del self.registry.records[key]

        self.assertEqual(
            self.utility._get_registry_stop_words(),
            ''
        )

    def test_empty_registry_no_error(self):
        self._set_record_value(u'')
        self.assertEqual(
            self.utility.get_snippets(u'some random text'),
            u''
        )

    def test_has_words_from_empty_registry(self):
        """Check that if the registry is empty has_stop_words returns False."""
        self._set_record_value(u'')
        self.assertFalse(
            self.utility.has_stop_words(u'some random text')
        )

    def test_has_words_from_registry(self):
        """Check that has_stop_words works with the registry."""
        self._set_record_value(u'random\nalert me\nlala')
        self.assertTrue(
            self.utility.has_stop_words(u'some random text')
        )

    def test_no_has_words_from_registry(self):
        """Check that has_stop_words works with the registry."""
        self._set_record_value(u'random\nalert me\nlala')
        self.assertFalse(
            self.utility.has_stop_words(u'some specific text')
        )

    def test_no_has_forbidden_words(self):
        """Check that has_forbidden_words returns False if the text
        does not have words from the forbidden_words registry
        """
        self._set_record_value(
            u'random\nalert me\nlala',
            record='forbidden_words'
        )
        self.assertFalse(
            self.utility.has_forbidden_words(u'some specific text')
        )

    def test_has_forbidden_words(self):
        """Check that has_forbidden_words returns True if the text has words
        from the forbidden_words registry
        """
        self._set_record_value(
            u'random\nalert me\nlala',
            record='forbidden_words'
        )
        self.assertFalse(
            self.utility.has_forbidden_words(u'some specific text')
        )

    def test_no_has_inadequate_words(self):
        """Check that has_inadequate_words returns False if the text
        does not have words from the inadequate_words registry
        """
        self._set_record_value(u'random\nalert me\nlala')
        self.assertFalse(
            self.utility.has_forbidden_words(u'some specific text')
        )

    def test_has_inadequate_words(self):
        """Check that has_inadequate_words returns True if the text has words
        from the inadequate_words registry
        """
        self._set_record_value(u'random\nalert me\nlala')
        self.assertFalse(
            self.utility.has_forbidden_words(u'some specific text')
        )

    def test_get_snippets_from_registry(self):
        """Check that get_snippets works with the registry."""
        self._set_record_value(u'random\nalert me\nlala')
        self.assertEqual(
            self.utility.get_snippets(u'some random text', chars=2),
            u'random\n\n...e random t...'
        )

    def test_no_get_snippets_from_registry(self):
        """Check that get_snippets works with the registry."""
        self._set_record_value(u'random\nalert me\nlala')
        self.assertEqual(
            self.utility.get_snippets(u'some specific text'),
            u''
        )

    def test_get_all_normalized_stop_words(self):
        """Check that if no register is specified words from both registries
        are used
        """
        self._set_all_records()
        normalized = self.utility.get_normalized_stop_words()
        self.assertIn(
            u'forbid',
            normalized
        )
        self.assertIn(
            u'inade',
            normalized
        )

    def test_get_forbidden_registry_normalized_stop_words(self):
        """Check that it returns only forbidden if that's passed as an argument
        """
        self._set_all_records()
        normalized = self.utility.get_normalized_stop_words(
            register='forbidden_words'
        )
        self.assertIn(
            u'forbid',
            normalized
        )
        self.assertNotIn(
            u'inade',
            normalized
        )

    def test_get_inadequate_registry_normalized_stop_words(self):
        """Check that it returns only inadequate if that's passed as an
        argument
        """
        self._set_all_records()
        normalized = self.utility.get_normalized_stop_words(
            register='inadequate_words'
        )
        self.assertNotIn(
            u'forbid',
            normalized
        )
        self.assertIn(
            u'inade',
            normalized
        )

    def test_invalid_registry_normalized_stop_words(self):
        """Check that no words are returned if an invalid registry is given"""
        self._set_all_records()
        normalized = self.utility.get_normalized_stop_words(
            register='non_existing_words'
        )
        self.assertEqual(
            normalized,
            []
        )

    def test_pass_list_registry_normalized_stop_words(self):
        """Check that passing a list also works"""
        self._set_all_records()
        normalized = self.utility.get_normalized_stop_words(
            register=('inadequate_words', )
        )
        self.assertNotIn(
            u'forbid',
            normalized
        )
        self.assertIn(
            u'inade',
            normalized
        )

    def test_has_forbidden_words_no_text(self):
        """Check that has_forbidden_words returns False if no text is provided
        """
        self.assertFalse(
            self.utility.has_forbidden_words('')
        )
        self.assertFalse(
            self.utility.has_forbidden_words(None)
        )

    def test_has_forbidden_words_no_words_in_registry(self):
        """Check that has_forbidden_words returns False if no words are found
        on the registry
        """
        self.assertIsNone(
            api.portal.get_registry_record(
                interface=IStopWords,
                name='forbidden_words'
            )
        )
        self.assertFalse(
            self.utility.has_forbidden_words('lalala')
        )

    def test_has_forbidden_words_no_words_found(self):
        """Check that has_forbidden_words returns False if no words from the
        registry are found on the text"""
        api.portal.set_registry_record(
            interface=IStopWords,
            name='forbidden_words',
            value=u'one\ntwo'
        )

        self.assertFalse(
            self.utility.has_forbidden_words('no words found')
        )

    def test_has_forbidden_words_words_found(self):
        """Check that has_forbidden_words returns True if words from the
        registry are found on the text
        """
        api.portal.set_registry_record(
            interface=IStopWords,
            name='forbidden_words',
            value=u'one\ntwo'
        )

        self.assertTrue(
            self.utility.has_forbidden_words('and now one is found!')
        )

    def test_has_inadequate_words_words_found(self):
        """Check that has_inadequate_words returns True if words from the
        registry are found on the text
        """
        api.portal.set_registry_record(
            interface=IStopWords,
            name='inadequate_words',
            value=u'one\ntwo'
        )

        self.assertTrue(
            self.utility.has_inadequate_words('and now one is found!')
        )


class HTMLNormalizeTestCase(unittest.TestCase):

    def test_regular_text_left_as_is(self):
        text = u'normal text'
        self.assertEqual(alert_text_normalize(text), text)

    def test_lower_case(self):
        text = u'UAU'
        self.assertEqual(alert_text_normalize(text), u'uau')

    def test_unicode_normalized_form(self):
        text = u'älert'
        self.assertEqual(alert_text_normalize(text), u'alert')

    def test_unicode_normalized_form_lower_case(self):
        text = u'Älert'
        self.assertEqual(alert_text_normalize(text), u'alert')

    def test_html_entity(self):
        text = u'alert&#220;s'
        self.assertEqual(alert_text_normalize(text), u'alertus')

    def test_html_entity_lower_case(self):
        text = u'alert&#252;s'
        self.assertEqual(alert_text_normalize(text), u'alertus')

    def test_multiple_spaces_on_source(self):
        text = u'alert     text'
        self.assertEqual(alert_text_normalize(text), u'alert text')

    def test_string(self):
        text = 'some string'
        self.assertEqual(alert_text_normalize(text), text)

    def test_string_umlauts(self):
        text = 'some \xfc'
        self.assertEqual(alert_text_normalize(text), u'some u')


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

    def test_different_line_endings(self):
        text = u'and one alert or second alert and even third alert on text'
        stop_words = u'one alert\r\nsecond alert\nthird alert'
        snippet_text = self.snippets(text, stop_words, chars=2)
        self.assertEqual(
            snippet_text,
            u'one alert, second alert, third alert'
            u'\n\n...d one alert o...'
            u'\n\n...r second alert a...'
            u'\n\n...n third alert o...'
        )

    def test_ignore_empty_lines(self):
        text = u'and one alert or text'
        stop_words = u'one alert\n\n\n\nsecond alert\nthird alert'
        snippet_text = self.snippets(text, stop_words, chars=2)
        self.assertEqual(
            snippet_text,
            u'one alert\n\n...d one alert o...'
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


class HasStopWordsTestCase(unittest.TestCase):

    def setUp(self):
        self.has_words = Alert().has_stop_words

    def test_no_text(self):
        text = None
        stop_words = u'one\ntwo'
        self.assertFalse(self.has_words(text, stop_words))

    def test_empty_text(self):
        text = u''
        stop_words = u'one\ntwo'
        self.assertFalse(self.has_words(text, stop_words))

    def test_no_stop_word_in_text(self):
        text = u'Random normal text'
        stop_words = u'one\ntwo'
        self.assertFalse(self.has_words(text, stop_words))

    def test_stop_word_in_text(self):
        text = u'Alerts two text'
        stop_words = u'one\ntwo'
        self.assertTrue(self.has_words(text, stop_words))


class GetTextFromObjectTest(unittest.TestCase):

    def test_contentish_like(self):
        """Dexterity content types and comments have a text method"""
        class DummyDXComment(object):

            @property
            def text(self):
                return 'found!'

        self.assertEqual(
            get_text_from_object(DummyDXComment()),
            'found!'
        )

    def test_event_with_contentish_like(self):
        """Content type wrapped in an event"""
        class DummyDX(object):

            @property
            def text(self):
                return 'found!'

        class DummyEventDX(object):

            @property
            def object(self):
                return DummyDX()

        self.assertEqual(
            get_text_from_object(DummyEventDX()),
            'found!'
        )

    def test_event_with_comment_like(self):
        """Comment wrapped in an event"""
        class DummyComment(object):

            @property
            def text(self):
                return 'found!'

        class DummyEventComment(object):

            @property
            def comment(self):
                return DummyComment()

        self.assertEqual(
            get_text_from_object(DummyEventComment()),
            'found!'
        )

    def test_something_else(self):
        """Something that does not have getText nor text"""
        class Dummy(object):
            pass

        self.assertEqual(
            get_text_from_object(Dummy()),
            ''
        )


class TestEntryDiff(unittest.TestCase):
    """Test c.contentalerts.handlers.get_new_entries"""

    def test_none_to_none(self):
        """What if both lists are none"""
        self.assertEqual(
            get_new_entries(None, None),
            [],
        )

    def test_something_to_none(self):
        """What if the list gets empty"""
        self.assertEqual(
            get_new_entries('one\ntwo', None),
            [],
        )

    def test_none_to_something(self):
        """What if the list was empty and now has some entries"""
        self.assertEqual(
            get_new_entries(None, 'one\ntwo'),
            ['one', 'two', ],
        )

    def test_none_to_only_newlines(self):
        """What if the list was empty and now has only newline characters"""
        self.assertEqual(
            get_new_entries(None, '\n\n\n\n'),
            [],
        )

    def test_something_to_same_something(self):
        """What if both, none empty, lists are the same"""
        self.assertEqual(
            get_new_entries('one\ntwo', 'one\ntwo'),
            [],
        )

    def test_something_plus_new_entries(self):
        """What if the new list has some new entries"""
        self.assertEqual(
            get_new_entries('one\ntwo', 'one\ntwo\nthree\nfour'),
            ['four', 'three', ],
        )

    def test_something_minus_some_entries(self):
        """What if the new list has removed some entries"""
        self.assertEqual(
            get_new_entries('one\ntwo\nthree\nfour', 'one\ntwo'),
            [],
        )

    def test_something_to_same_something_but_different_order(self):
        """What if both lists have the same entries but ordered differently"""
        self.assertEqual(
            get_new_entries('one\ntwo\nthree\nfour', 'three\none\nfour\ntwo'),
            [],
        )

    def test_something_plus_newline_characters(self):
        """What if the new list only adds newline characters"""
        self.assertEqual(
            get_new_entries('one\ntwo', '\n\n\n\none\ntwo\n\n\n\n'),
            [],
        )

    def test_something_minus_newline_characters(self):
        """What if the new list only removes newline characters"""
        self.assertEqual(
            get_new_entries('\n\n\n\none\ntwo\n\n\n\n', 'one\ntwo'),
            [],
        )

    def test_something_plus_some_minus_some_others(self):
        """What if the new list has new entries and some entries removed"""
        self.assertEqual(
            get_new_entries('one\ntwo\nthree\nfour', 'one\ntwo\nthree\nfive'),
            [u'five', ],
        )


class VerifyBrainTestCase(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # create the document and attach the marker interface
        self.doc = api.content.create(
            container=self.portal,
            id='document-test',
            title='Document 1',
            type='Document',
            text='Some random text'
        )

    def test_stop_word_not_in_object(self):
        """Check that the verified marker interface is kept

        It should be removed only if the stop words are found on the object's
        text.
        """
        alsoProvides(self.doc, IStopWordsVerified)
        self.doc.reindexObject()

        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(id=self.doc.id)[0]

        verify_brain(brain, new_entries='else')

        self.assertTrue(IStopWordsVerified.providedBy(self.doc))
        self.assertFalse(IHasStopWords.providedBy(self.doc))

    def test_stop_word_in_object(self):
        """Check that the verified marker interface is removed

        It should be removed if the stop words are found on the object's text.
        """
        alsoProvides(self.doc, IStopWordsVerified)
        self.doc.reindexObject()

        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(id=self.doc.id)[0]

        verify_brain(brain, new_entries='random')

        self.assertFalse(IStopWordsVerified.providedBy(self.doc))
        self.assertTrue(IHasStopWords.providedBy(self.doc))

    def test_object_without_verified_marker_interface(self):
        """Corner case: the object does not have the verified marker interface

        It should add the stop words marker interface without raising any
        exception.
        """
        self.assertFalse(IStopWordsVerified.providedBy(self.doc))
        self.assertFalse(IHasStopWords.providedBy(self.doc))

        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(id=self.doc.id)[0]

        verify_brain(brain, new_entries='random')

        self.assertFalse(IStopWordsVerified.providedBy(self.doc))
        self.assertTrue(IHasStopWords.providedBy(self.doc))

    def test_no_brain(self):
        """Corner case: verify_brain does not get a brain but something else

        It should return silently.
        """
        self.assertIsNone(
            verify_brain(self.doc, new_entries='random')
        )

    def test_no_entries(self):
        """Corner case: verify_brain gets an empty string as new entries

        It should return silently.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(id=self.doc.id)[0]
        self.assertIsNone(
            verify_brain(brain, new_entries='')
        )

    def test_none_entries(self):
        """Corner case: verify_brain gets None as new entries

        It should return silently.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(id=self.doc.id)[0]
        self.assertIsNone(
            verify_brain(brain, new_entries=None)
        )
