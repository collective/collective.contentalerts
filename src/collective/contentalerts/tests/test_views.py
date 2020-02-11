# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from collective.taskqueue.interfaces import ITaskQueueLayer
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
            type='Document',
            text='lala'
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


class ReviewObjectsView(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        alsoProvides(self.request, ITaskQueueLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def _get_view(self):
        return api.content.get_view(
            name='review-objects',
            context=self.portal,
            request=self.request
        )

    def _create_document(self, text):
        if not text:
            text = 'lala'
        doc = api.content.create(
            container=self.portal,
            type='Document',
            id='doc',
            text=text
        )
        return doc

    def set_default_workflow(self):
        """Document objects created in this test do not have a workflow
        attached, add a default one for the tests that require that.
        """
        workflow_tool = api.portal.get_tool('portal_workflow')
        workflow_tool.setDefaultChain('simple_publication_workflow')

    def test_only_start_parameter(self):
        self.request.set('start', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_only_size_parameter(self):
        self.request.set('size', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_only_entries_parameter(self):
        self.request.set('entries', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_missing_entries_parameter(self):
        self.request.set('start', '2')
        self.request.set('size', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_missing_size_parameter(self):
        self.request.set('start', '2')
        self.request.set('entries', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_missing_start_parameter(self):
        self.request.set('size', '2')
        self.request.set('entries', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_invalid_start_parameter_value(self):
        self.request.set('start', '2a')
        self.request.set('size', '2')
        self.request.set('entries', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_invalid_size_parameter_value(self):
        self.request.set('start', '2')
        self.request.set('size', '2a')
        self.request.set('entries', '2')
        self.assertRaises(
            ValueError,
            self._get_view()._check_parameters
        )

    def test_parameters_converted(self):
        self.request.set('start', '2')
        self.request.set('size', '3')
        self.request.set('entries', 'lala%0Amagic')
        start, size, entries = self._get_view()._check_parameters()

        self.assertEqual(
            start,
            2
        )
        self.assertEqual(
            size,
            3
        )
        self.assertEqual(
            entries,
            'lala\nmagic'
        )

    def test_object_verified(self):
        """Create a document and call the view. The document should have the
        IHasStopWords marker interface attached
        """
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)
        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self._get_view()()

        self.assertTrue(
            IHasStopWords.providedBy(doc)
        )

    def test_verify_unknown_type_no_interface(self):
        """Create a document and call the view

        But do so with a type parameter that the Document does not have, so
        no marker interface is applied.
        """
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)
        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self.request.set('type', 'document.action.action')
        self._get_view()()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

    def test_verify_known_type_add_interface(self):
        """Create a document and call the view

        Specify a marker interface that Document provides, to check that
        filtering by marker interfaces works.
        """
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)

        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self.request.set(
            'type',
            'Products.CMFCore.interfaces.IContentish',
        )
        self._get_view()()

        self.assertTrue(
            IHasStopWords.providedBy(doc)
        )

    def test_verify_unknown_state_no_interface(self):
        """Create a document and call the view

        But do so with a workflow state that the Document does not have, so
        no marker interface is applied.
        """
        self.set_default_workflow()
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)
        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self.request.set('states', 'non-existing')
        self._get_view()()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

    def test_verify_known_state_add_interface(self):
        """Create a document and call the view

        Specify the Document workflow state , to check that filtering by
        workflow state works.
        """
        self.set_default_workflow()
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)

        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self.request.set('states', 'private')
        self._get_view()()

        self.assertTrue(
            IHasStopWords.providedBy(doc)
        )

    def test_verify_known_multiple_states_add_interface(self):
        """Create a document and call the view

        Specify multiple workflow states (including the Document one), to
        check that filtering by workflow state works.
        """
        self.set_default_workflow()
        doc = self._create_document('Document with fishy content')
        alsoProvides(doc, IStopWordsVerified)

        doc.reindexObject()

        self.assertFalse(
            IHasStopWords.providedBy(doc)
        )

        self.request.set('start', '0')
        self.request.set('size', '3')
        self.request.set('entries', 'fishy')
        self.request.set('states', 'private,published')
        self._get_view()()

        self.assertTrue(
            IHasStopWords.providedBy(doc)
        )
