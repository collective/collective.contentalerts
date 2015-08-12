# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import collective.contentalerts


class CollectiveContentalertsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.contentalerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contentalerts:default')


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
