# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWords
from collective.contentalerts.testing import COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest


class GenericSetupTest(unittest.TestCase):
    layer = COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_forbidden_registry_record(self):
        """Check that the registry record exists."""
        record = 'forbidden_words'
        self.assertIsNone(
            api.portal.get_registry_record(
                interface=IStopWords,
                name=record
            )
        )

    def test_inadequate_registry_record(self):
        """Check that the registry record exists."""
        record = 'inadequate_words'
        self.assertIsNone(
            api.portal.get_registry_record(
                interface=IStopWords,
                name=record
            )
        )

    def test_roles_with_permission(self):
        """Check that the permission is given to the appropriate roles."""
        permission = 'collective.contentalerts: Edit stop words'
        roles = [
            r['name']
            for r in self.portal.rolesOfPermission(permission)
            if r['selected']
        ]
        self.assertIn('Manager', roles)
        self.assertIn('Site Administrator', roles)

    def test_controlpanel_view(self):
        """Check that the controlpanel view for stop words exist."""
        view = getMultiAdapter(
            (self.portal, self.request),
            name='stop-words-settings'
        )
        self.assertTrue(view())

    def test_controlpanel_registered(self):
        """Check that the control panel is registered on the tool."""
        control_panel_tool = api.portal.get_tool('portal_controlpanel')
        actions_ids = [
            configlet.id
            for configlet in control_panel_tool.listActions()
        ]
        self.assertIn(
            'collective.contentalerts.settings',
            actions_ids
        )
