# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest


class TestVerifiedInterfaceHandler(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # set some stop words
        api.portal.set_registry_record(
            name='stop_words',
            interface=IStopWords,
            value=u'lala\nlili'
        )
        # create the document and attach the marker interface
        self.doc = api.content.create(
            container=self.portal,
            id='test',
            title='Document 1',
            type='Document',
        )
        self.doc.setText('Some random text')
        alsoProvides(self.doc, IStopWordsVerified)
        self.doc.reindexObject()

    def test_no_new_word_added(self):
        """If a document has IStopWordsVerified interface and no new stop word
        is added, the document keeps the interface
        """
        # remove one stop_word
        api.portal.set_registry_record(
            name='stop_words',
            interface=IStopWords,
            value=u'lala\n'
        )

        # the document still keeps the interface
        self.assertTrue(
            IStopWordsVerified.providedBy(self.doc)
        )

    def test_new_word_added_and_not_in_document(self):
        """If a document has IStopWordsVerified interface and a new stop word
        is added, but is not on the document, it keeps the interface
        """
        # add one stop_word
        api.portal.set_registry_record(
            name='stop_words',
            interface=IStopWords,
            value=u'lala\nmagic'
        )

        # the document keeps the interface
        self.assertTrue(
            IStopWordsVerified.providedBy(self.doc)
        )

    def test_new_word_added_and_in_document(self):
        """If a document has IStopWordsVerified interface and a new stop word
        added is also on the document, the marker interface is removed
        """
        # add one stop_word
        api.portal.set_registry_record(
            name='stop_words',
            interface=IStopWords,
            value=u'lala\nrandom'
        )

        # the document no longer keeps the interface
        self.assertFalse(
            IStopWordsVerified.providedBy(self.doc)
        )
