# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.contentalerts


class CollectiveContentalertsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.contentalerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contentalerts:default')


COLLECTIVE_CONTENTALERTS_FIXTURE = CollectiveContentalertsLayer()


COLLECTIVE_CONTENTALERTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTALERTS_FIXTURE,),
    name='CollectiveContentalertsLayer:IntegrationTesting'
)


COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENTALERTS_FIXTURE,),
    name='CollectiveContentalertsLayer:FunctionalTesting'
)


COLLECTIVE_CONTENTALERTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CONTENTALERTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveContentalertsLayer:AcceptanceTesting'
)
