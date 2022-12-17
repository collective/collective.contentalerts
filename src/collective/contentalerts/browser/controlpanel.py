from collective.contentalerts import _
from collective.contentalerts.interfaces import IStopWords
from plone.app.registry.browser import controlpanel


class ControlPanelForm(controlpanel.RegistryEditForm):

    schema = IStopWords
    label = _("stop_words_controlpanel_settings_label", default="Stop words")
    description = _(
        "stop_words_controlpanel_settings_description", default="Edit stop words."
    )


class ControlPanelView(controlpanel.ControlPanelFormWrapper):

    form = ControlPanelForm
