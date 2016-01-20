# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager

import collective.contentalerts
import doctest


class CollectiveContentalertsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.contentalerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contentalerts:default')

        # Configure mock mail host
        site_manager = getSiteManager(portal)
        site_manager.unregisterUtility(provided=IMailHost)
        mail_host = MockMailHost('MailHost')
        site_manager.registerUtility(mail_host, IMailHost)
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mail_host

    def tearDownPloneSite(self, portal):
        site_manager = getSiteManager(portal)
        portal.MailHost = portal._original_MailHost
        site_manager.unregisterUtility(provided=IMailHost)
        site_manager.registerUtility(
            aq_base(portal._original_MailHost),
            provided=IMailHost
        )


class CollectiveContentalertsDexterityLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.contentalerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contentalerts:default')


COLLECTIVE_CONTENTALERTS_FIXTURE = CollectiveContentalertsLayer()
COLLECTIVE_CONTENTALERTS_DEXTERITY_FIXTURE = CollectiveContentalertsDexterityLayer()  # noqa


COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTALERTS_FIXTURE,),
    name='CollectiveContentalertsLayer:IntegrationTesting'
)
COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENTALERTS_FIXTURE,),
    name='CollectiveContentalertsLayer:FunctionalTesting'
)
COLLECTIVE_CONTENTALERTS_DEXTERITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTALERTS_DEXTERITY_FIXTURE,),
    name='CollectiveContentalertsDexterityLayer:IntegrationTesting'
)

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
