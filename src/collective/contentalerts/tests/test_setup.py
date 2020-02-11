# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.contentalerts.interfaces import ICollectiveContentalertsLayer
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone.browserlayer import utils
from Products.CMFPlone.utils import get_installer

import unittest


PKG_NAME = 'collective.contentalerts'


class TestSetup(unittest.TestCase):
    """Test that collective.contentalerts is properly installed."""

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = get_installer(self.portal, self.request)

    def test_product_installed(self):
        """Test if the add-on is installed with portal_quickinstaller."""
        self.assertTrue(
            self.installer.is_product_installed(PKG_NAME)
        )

    def test_browserlayer(self):
        """Test that ICollectiveContentalertsLayer is registered."""
        self.assertIn(ICollectiveContentalertsLayer, utils.registered_layers())

    def test_product_uninstalled(self):
        """Test if collective.contentalerts is cleanly uninstalled."""
        self.installer.uninstall_product(PKG_NAME)
        self.assertFalse(
            self.installer.is_product_installed(PKG_NAME)
        )
