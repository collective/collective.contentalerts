# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.contentalerts.interfaces import ICollectiveContentalertsLayer
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.browserlayer import utils

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.contentalerts is properly installed."""

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if the add-on is installed with portal_quickinstaller."""
        self.assertTrue(
            self.installer.isProductInstalled('collective.contentalerts')
        )

    def test_browserlayer(self):
        """Test that ICollectiveContentalertsLayer is registered."""
        self.assertIn(ICollectiveContentalertsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.contentalerts'])

    def test_product_uninstalled(self):
        """Test if collective.contentalerts is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled('collective.contentalerts')
        )
