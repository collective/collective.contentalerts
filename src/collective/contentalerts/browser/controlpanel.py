# -*- coding: utf-8 -*-
from collective.contentalerts import _
from collective.contentalerts.interfaces import IStopWords
from plone.app.registry.browser import controlpanel


class ControlPanelForm(controlpanel.RegistryEditForm):

    schema = IStopWords
    label = _(
        u'blacklist_words_controlpanel_settings_label',
        default=u'Blacklist words'
    )
    description = _(
        u'blacklist_words_controlpanel_settings_description',
        default=u'Edit blacklist words.'
    )


class ControlPanelView(controlpanel.ControlPanelFormWrapper):

    form = ControlPanelForm
