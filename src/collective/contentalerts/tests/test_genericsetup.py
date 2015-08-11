# -*- coding: utf-8 -*-
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class GenericSetupTest(unittest.TestCase):
    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_registry_record(self):
        """Check that the registry record exists."""
        registry = getUtility(IRegistry)
        self.assertIn(
            'collective.contentalerts.interfaces.IStopWords.stop_words',
            registry
        )
