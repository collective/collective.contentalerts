# -*- coding: utf-8 -*-
from collective.contentalerts import _
from collective.contentalerts.interfaces import IStopWords
from plone.app.registry.browser import controlpanel


class ControlPanelForm(controlpanel.RegistryEditForm):

    schema = IStopWords
    label = _(
        u'stop_words_controlpanel_settings_label',
        default=u'Stop words'
    )
    description = _(
        u'stop_words_controlpanel_settings_description',
        default=u'Edit stop words.'
    )


class ControlPanelView(controlpanel.ControlPanelFormWrapper):

    form = ControlPanelForm
