# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.discussion.interfaces import IConversation
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import createObject
from zope.interface import alsoProvides

import unittest


class DiscardAlertsViewTestCase(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.document = api.content.create(
            container=self.portal,
            id='doc1',
            title='Document 1',
            type='Document'
        )

    def test_no_interface_no_problem(self):
        """Calling @@discard-alert on a document that does not have the
        IHasStopWords interface does not break.
        it."""
        discard_view = api.content.get_view(
            name='discard-alert',
            context=self.document,
            request=self.request
        )
        discard_view()

        self.assertFalse(IHasStopWords.providedBy(self.document))

    def test_remove_interface_on_a_document(self):
        """Calling @@discard-alert on a document that has the IHasStopWords
        removes it and adds the IStopWordsVerified marker interface"""
        alsoProvides(self.document, IHasStopWords)
        self.assertTrue(IHasStopWords.providedBy(self.document))

        discard_view = api.content.get_view(
            name='discard-alert',
            context=self.document,
            request=self.request
        )
        discard_view()

        self.assertFalse(IHasStopWords.providedBy(self.document))
        self.assertTrue(IStopWordsVerified.providedBy(self.document))

    def test_remove_interface_on_a_comment(self):
        """Calling @@discard-alert on a comment that has the IHasStopWords
        removes it and adds the IStopWordsVerified marker interface"""
        comment = createObject('plone.Comment')
        comment.text = 'something'
        comment.author_username = 'jim'
        comment.author_name = 'Jim'
        comment.author_email = 'jim@example.com'
        conversation = IConversation(self.document)
        conversation.addComment(comment)

        alsoProvides(comment, IHasStopWords)
        self.assertTrue(IHasStopWords.providedBy(comment))

        discard_view = api.content.get_view(
            name='discard-alert',
            context=comment,
            request=self.request
        )
        discard_view()

        self.assertFalse(IHasStopWords.providedBy(comment))
        self.assertTrue(IStopWordsVerified.providedBy(comment))

    def test_redirect(self):
        self.assertNotIn('location', self.request.response.headers)
        discard_view = api.content.get_view(
            name='discard-alert',
            context=self.document,
            request=self.request
        )
        discard_view()
        self.assertEqual(
            self.document.absolute_url(),
            self.request.response.headers['location']
        )

    def test_message(self):
        """If the interface gets removed, a portal message is shown."""
        alsoProvides(self.document, IHasStopWords)
        discard_view = api.content.get_view(
            name='discard-alert',
            context=self.document,
            request=self.request
        )
        discard_view()
        messages = IStatusMessage(self.request)
        show = messages.show()
        self.assertEqual(len(show), 1)
        self.assertIn('The object no longer ', show[0].message)

    def test_no_message(self):
        """If no interface gets removed, no portal message is shown."""
        discard_view = api.content.get_view(
            name='discard-alert',
            context=self.document,
            request=self.request
        )
        discard_view()
        messages = IStatusMessage(self.request)
        show = messages.show()
        self.assertEqual(len(show), 0)
