# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from collective.contentalerts import _
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import ITextAlertCondition
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implementer


class TextAlertConditionExecutor(object):
    """The executor for this condition."""
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        text = None

        # if it's a comment
        if getattr(self.event, 'comment', None):
            if getattr(self.event.comment, 'text', None):
                text = self.event.comment.text
        # if it's a AT/DX
        elif getattr(self.event, 'object', None):
            if getattr(self.event.object, 'getText', None):
                text = self.event.object.getText()
            elif getattr(self.event.object, 'text', None):
                text = self.event.object.text

        if not text:
            return False

        stop_words = self.element.stop_words
        if stop_words is None or stop_words.strip() == u'':
            stop_words = None
        else:
            request = self.context.REQUEST
            request.set('stop_words', stop_words)

        alert_utility = getUtility(IAlert)

        return alert_utility.has_stop_words(text, stop_words=stop_words)


@implementer(ITextAlertCondition, IRuleElementData)
class TextAlertCondition(SimpleItem):
    """The persistent implementation of the text alert condition."""
    stop_words = None
    element = 'collective.contentalerts.TextAlert'

    @property
    def summary(self):
        return _(
            u'contentrules_text_alert_condition_summary',
            default=u'Provide a stop words list, one per line, or leave it '
                    u'empty to use the shared one (registry based).'
        )


class TextAlertConditionAddForm(AddForm):
    form_fields = form.FormFields(ITextAlertCondition)
    label = _(u'Add a text alert condition')
    description = _(u'A text alert condition makes the rule apply '
                    u'only if there are stop words on the object\'s text.')
    form_name = _(u'Configure element')

    def create(self, data):
        condition = TextAlertCondition()
        form.applyChanges(condition, self.form_fields, data)
        return condition


class TextAlertConditionEditForm(EditForm):
    form_fields = form.FormFields(ITextAlertCondition)
    label = _(u'Edit a text alert condition')
    description = _(u'A text alert condition makes the rule apply '
                    u'only if there are stop words on the object\'s text.')
    form_name = _(u'Configure element')
