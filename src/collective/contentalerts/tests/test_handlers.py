# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_ASYNC_FUNCTIONAL_TESTING  # noqa
from collective.taskqueue.interfaces import ITaskQueue
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.interface import alsoProvides

import transaction
import unittest


class TestVerifiedInterfaceHandler(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_ASYNC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # set some stop words
        api.portal.set_registry_record(
            name='inadequate_words',
            interface=IStopWords,
            value=u'lala\nlili'
        )
        # create the document and attach the marker interface
        self.doc = api.content.create(
            container=self.portal,
            id='test',
            title='Document 1',
            type='Document',
            text='Some random text'
        )
        alsoProvides(self.doc, IStopWordsVerified)
        self.doc.reindexObject()

    def test_no_new_word_added(self):
        """If the stop words list is updated but no new words are added, no
        async job is queued
        """
        # remove one stop_word
        api.portal.set_registry_record(
            name='inadequate_words',
            interface=IStopWords,
            value=u'lala\n'
        )

        # tasks are only queued on a successful transaction
        transaction.commit()
        self.assertEqual(
            len(getUtility(ITaskQueue, name='test-queue')),
            0,
        )

    def test_new_word_added(self):
        """If the stop words list is updated and new words are added, an
        async job is queued
        """
        # add one stop_word
        api.portal.set_registry_record(
            name='inadequate_words',
            interface=IStopWords,
            value=u'lala\nmagic'
        )

        # tasks are only queued on a successful transaction
        transaction.commit()
        taskqueue = getUtility(ITaskQueue, name='test-queue')
        self.assertEqual(
            len(taskqueue),
            1,
        )

        task = taskqueue.get()
        self.assertIn(
            'size=300',
            task['url']
        )
        self.assertIn(
            'start=0',
            task['url']
        )
        self.assertIn(
            'entries=magic',
            task['url']
        )

    def test_new_word_with_spaces_added(self):
        """Check that the new words are correctly URL encoded"""
        # add one stop_word with spaces
        api.portal.set_registry_record(
            name='inadequate_words',
            interface=IStopWords,
            value=u'lala\nmagic powers & more'
        )

        # tasks are only queued on a successful transaction
        transaction.commit()
        taskqueue = getUtility(ITaskQueue, name='test-queue')
        task = taskqueue.get()
        self.assertIn(
            'size=300',
            task['url']
        )
        self.assertIn(
            'start=0',
            task['url']
        )
        self.assertIn(
            'entries=magic+powers+%26+more',
            task['url']
        )

    def test_new_forbidden_word(self):
        """Check that with forbidden words work as well"""
        api.portal.set_registry_record(
            name='forbidden_words',
            interface=IStopWords,
            value=u'lala\nmagic'
        )

        # tasks are only queued on a successful transaction
        transaction.commit()
        taskqueue = getUtility(ITaskQueue, name='test-queue')
        task = taskqueue.get()
        self.assertIn(
            'size=300',
            task['url']
        )
        self.assertIn(
            'start=0',
            task['url']
        )
        self.assertIn(
            'entries=lala%0Amagic',
            task['url']
        )
