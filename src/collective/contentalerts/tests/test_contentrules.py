# -*- coding: utf-8 -*-
from collective.contentalerts.contentrules import ForbiddenTextAlertCondition
from collective.contentalerts.contentrules import InadequateTextAlertCondition
from collective.contentalerts.contentrules import TextAlertCondition
from collective.contentalerts.contentrules import TextAlertConditionEditFormView  # noqa
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING  # noqa
from plone import api
from plone.app.contentrules.rule import Rule
from plone.app.discussion.interfaces import IConversation
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleCondition
from plone.stringinterp.interfaces import IStringSubstitution
from Testing.ZopeTestCase.utils import setupCoreSessions
from zope.component import createObject
from zope.component import getAdapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer

import unittest


@implementer(IObjectEvent)
class CommentDummyEvent(object):

    def __init__(self, obj):
        self.comment = obj


@implementer(IObjectEvent)
class ContentTypeDummyEvent(object):

    def __init__(self, obj):
        self.object = obj


class TextAlertConditionTestCase(unittest.TestCase):
    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.name = 'collective.contentalerts.TextAlert'
        self.element = getUtility(
            IRuleCondition,
            name=self.name
        )

        self.document = api.content.create(
            container=self.portal,
            id='doc1',
            title='Document 1',
            type='Document',
            text='lala',
        )

    def _add_comment(self, text):
        comment = createObject('plone.Comment')
        comment.text = text
        comment.author_username = 'jim'
        comment.author_name = 'Jim'
        comment.author_email = 'jim@example.com'
        conversation = IConversation(self.document)
        conversation.addComment(comment)
        return comment

    def _set_record_value(self, value, record='inadequate_words'):
        api.portal.set_registry_record(
            name=record,
            interface=IStopWords,
            value=value
        )

    def test_registered(self):
        self.assertEqual(self.name, self.element.addview)
        self.assertEqual('edit', self.element.editview)
        self.assertEqual(None, self.element.for_)
        self.assertEqual(IObjectEvent, self.element.event)

    def test_add_view_no_data(self):
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter(
            (rule, self.portal.REQUEST),
            name='+condition'
        )
        add_view = getMultiAdapter(
            (adding, self.portal.REQUEST),
            name=self.element.addview
        )

        add_view.form_instance.update()
        content = add_view.form_instance.create(data={})
        add_view.form_instance.add(content)

        condition = rule.conditions[0]
        self.assertTrue(isinstance(condition, TextAlertCondition))
        self.assertEqual(condition.stop_words, None)

    def test_add_view_with_stop_words(self):
        stop_words = u'alert\nanother alert\nlast one'
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter(
            (rule, self.portal.REQUEST),
            name='+condition'
        )
        add_view = getMultiAdapter(
            (adding, self.portal.REQUEST),
            name=self.element.addview
        )

        add_view.form_instance.update()
        content = add_view.form_instance.create(
            data={'stop_words': stop_words}
        )
        add_view.form_instance.add(content)

        condition = rule.conditions[0]
        self.assertTrue(isinstance(condition, TextAlertCondition))
        self.assertEqual(
            condition.stop_words,
            stop_words
        )

    def test_edit_view(self):
        condition = TextAlertCondition()
        edit_view = getMultiAdapter(
            (condition, self.request),
            name=self.element.editview
        )
        self.assertTrue(
            isinstance(edit_view, TextAlertConditionEditFormView)
        )

    def test_empty_text_no_condition(self):
        comment = self._add_comment('')
        condition = TextAlertCondition()

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_no_text_no_condition(self):
        comment = self._add_comment(None)
        condition = TextAlertCondition()

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_regular_text_no_local_no_registry_stop_words(self):
        comment = self._add_comment('regular text')
        condition = TextAlertCondition()

        self.assertEqual(
            getUtility(IAlert)._get_registry_stop_words(),
            ''
        )
        self.assertEqual(condition.stop_words, None)

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_regular_text_no_local_stop_words_and_registry_stop_words(self):
        comment = self._add_comment('regular text')
        condition = TextAlertCondition()

        self.assertEqual(
            getUtility(IAlert)._get_registry_stop_words(),
            ''
        )
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_regular_text_local_stop_words_and_no_registry_stop_words(self):
        comment = self._add_comment('regular text')
        condition = TextAlertCondition()

        self._set_record_value(u'one alert\nanother alert')
        self.assertEqual(condition.stop_words, None)

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_regular_text_local_and_registry_stop_words(self):
        comment = self._add_comment('regular text')
        condition = TextAlertCondition()

        self._set_record_value(u'yet another\nlast one')
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_alert_text_no_local_stop_words_and_registry_stop_words(self):
        comment = self._add_comment('this gives one alert')
        condition = TextAlertCondition()

        self._set_record_value(u'one alert\nanother alert')
        self.assertEqual(condition.stop_words, None)

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertTrue(executable())

    def test_alert_text_local_stop_words_no_registry_stop_words(self):
        comment = self._add_comment('this gives one alert')
        condition = TextAlertCondition()

        self.assertEqual(
            getUtility(IAlert)._get_registry_stop_words(),
            ''
        )
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertTrue(executable())

    def test_alert_text_local_and_registry_stop_words(self):
        comment = self._add_comment('this gives one alert')
        condition = TextAlertCondition()

        self._set_record_value(u'almost\nlast one')
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertTrue(executable())

    def test_alert_text_local_stop_words_shadow_registry_stop_words(self):
        """Local stop words list shadows the registry stop words.

        This basically means that if the text contains stop words from
        the registry, but there is a local stop words list that does not
        complain, the text will be reported that it does *not* contain stop
        words.

        That's a way to override the general stop words list to provide a
        completely different set of stop words.
        """
        comment = self._add_comment('this should give one alert')
        condition = TextAlertCondition()

        self._set_record_value(u'one alert\nanother alert')
        condition.stop_words = u'almost\nlast one'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        self.assertFalse(executable())

    def test_document(self):
        document = api.content.create(
            container=self.portal,
            id='doc2',
            title='Document 2',
            type='Document',
            text='this gives one alert',
        )
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, ContentTypeDummyEvent(document)),
            IExecutable
        )
        self.assertTrue(executable())

    def test_stop_words_on_request(self):
        comment = self._add_comment('whatever')
        condition = TextAlertCondition()

        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        self.assertEqual(
            self.request.get('stop_words'),
            condition.stop_words
        )

    def test_stop_words_not_in_request(self):
        comment = self._add_comment('whatever')
        condition = TextAlertCondition()

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        self.assertIsNone(self.request.get('stop_words'))

    def test_has_stop_words_add_interface_comment(self):
        comment = self._add_comment('one alert')
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        self.assertTrue(IHasStopWords.providedBy(comment))

    def test_has_stop_words_add_interface_document(self):
        document = api.content.create(
            container=self.portal,
            id='doc2',
            title='Document 2',
            type='Document',
            text='this gives one alert'
        )
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, ContentTypeDummyEvent(document)),
            IExecutable
        )
        executable()
        self.assertTrue(IHasStopWords.providedBy(document))

    def test_no_stop_words_no_interface(self):
        comment = self._add_comment('no alert')
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        self.assertFalse(IHasStopWords.providedBy(comment))

    def test_add_and_remove_interface(self):
        comment = self._add_comment('one alert')
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        # adds the marker interface
        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()

        comment.text = 'no longer creating an alert'
        executable()
        self.assertFalse(IHasStopWords.providedBy(comment))

    def test_has_stop_words_add_interface_document_on_catalog(self):
        document = api.content.create(
            container=self.portal,
            id='doc2',
            title='Document 2',
            type='Document',
            text='this gives one alert'
        )
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, ContentTypeDummyEvent(document)),
            IExecutable
        )
        executable()
        brains = api.content.find(
            self.portal,
            object_provides=IHasStopWords.__identifier__
        )
        self.assertEqual(len(brains), 1)

    def test_no_stop_words_no_interface_on_catalog(self):
        comment = self._add_comment('no alert')
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        brains = api.content.find(
            self.portal,
            object_provides=IHasStopWords.__identifier__
        )
        self.assertEqual(len(brains), 0)

    def test_add_and_remove_interface_on_catalog(self):
        self._add_comment('one alert')
        # acquisition wrapped version of the comment
        comment = IConversation(self.document).values()[0]
        condition = TextAlertCondition()
        condition.stop_words = u'one alert\nanother alert'

        # adds the marker interface
        executable = getMultiAdapter(
            (self.portal, condition, CommentDummyEvent(comment)),
            IExecutable
        )
        executable()
        brains = api.content.find(
            self.portal,
            object_provides=IHasStopWords.__identifier__
        )
        self.assertEqual(len(brains), 1)

        comment.text = 'no longer creating an alert'
        executable()
        brains = api.content.find(
            self.portal,
            object_provides=IHasStopWords.__identifier__
        )
        self.assertEqual(len(brains), 0)


class SpecificAlertConditionsTestCase(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def _set_record_value(self, value, record='inadequate_words'):
        api.portal.set_registry_record(
            name=record,
            interface=IStopWords,
            value=value
        )

    def test_inadequate_condition(self):
        document = api.content.create(
            container=self.portal,
            id='doc2',
            title='Document 2',
            type='Document',
            text='this gives one alert'
        )
        condition = InadequateTextAlertCondition()
        self._set_record_value(u'one')

        executable = getMultiAdapter(
            (self.portal, condition, ContentTypeDummyEvent(document)),
            IExecutable
        )
        self.assertTrue(executable())

    def test_forbidden_condition(self):
        document = api.content.create(
            container=self.portal,
            id='doc2',
            title='Document 2',
            type='Document',
            text='this gives one alert'
        )
        condition = ForbiddenTextAlertCondition()
        self._set_record_value(u'one', record='forbidden_words')

        executable = getMultiAdapter(
            (self.portal, condition, ContentTypeDummyEvent(document)),
            IExecutable
        )
        self.assertTrue(executable())


class ContentRulesSubstitutionsTest(unittest.TestCase):
    layer = COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING

    def setUp(self):
        setupCoreSessions(self.layer['app'])

        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.document = api.content.create(
            container=self.portal,
            id='doc1',
            title='Document 1',
            type='Document',
            text='lala'
        )

    def _add_comment(self, text='lilala'):
        comment = createObject('plone.Comment')
        comment.text = text
        comment.author_username = 'jim'
        comment.author_name = 'Jim'
        comment.author_email = 'jim@example.com'
        conversation = IConversation(self.document)
        conversation.addComment(comment)

    def test_stop_words_on_request(self):
        stop_words = 'hi\nI am around'
        self.request.set('stop_words', stop_words)
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'text_alert'
        )
        self.assertEqual(
            text_alert._get_stop_words(),
            stop_words
        )

    def test_no_stop_words_on_request(self):
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'text_alert'
        )
        self.assertIsNone(text_alert._get_stop_words())

    def test_get_text_from_comment(self):
        text = 'some random text'
        self._add_comment(text=text)
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'comment_alert'
        )
        self.assertEqual(
            text_alert._get_text(),
            text
        )

    def test_no_comment_no_text(self):
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'comment_alert'
        )
        self.assertEqual(
            text_alert._get_text(),
            u''
        )

    def test_get_text_from_document(self):
        text = 'some random text'
        self.document.text = text
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'text_alert'
        )
        self.assertIn(
            text,
            text_alert._get_text(),
        )

    def test_get_snippet(self):
        stop_words = 'hi\nalert'
        self.request.set('stop_words', stop_words)
        self.document.text = 'Some text that contains an alert and more'
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'text_alert'
        )
        self.assertNotEqual(text_alert().find('alert'), -1)

    def test_no_snippet(self):
        self.document.text = 'Some text that contains an alert and more'
        text_alert = getAdapter(
            self.document,
            IStringSubstitution,
            name=u'text_alert'
        )
        self.assertEqual(
            text_alert(),
            u'',
        )
