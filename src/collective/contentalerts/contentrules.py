# -*- coding: utf-8 -*-
from collective.contentalerts import _
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import IForbiddenTextAlertCondition
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IInadequateTextAlertCondition
from collective.contentalerts.interfaces import ITextAlertCondition
from collective.contentalerts.utilities import get_text_from_object
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.adapters import BaseSubstitution
from z3c.form import form
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import noLongerProvides


class TextAlertConditionExecutor(object):
    """The executor for this condition."""
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        return self.check()

    def check(self, forbidden=False, inadequate=False):
        text = get_text_from_object(self.event)
        if not text:
            return False

        alert_utility = getUtility(IAlert)

        if forbidden or inadequate:
            has_words = alert_utility.has_stop_words(text)
            if forbidden:
                ret_value = alert_utility.has_forbidden_words(text)
            else:
                ret_value = alert_utility.has_inadequate_words(text)
        else:
            stop_words = self.element.stop_words
            if stop_words is None or stop_words.strip() == u'':
                stop_words = None
            else:
                request = self.context.REQUEST
                request.set('stop_words', stop_words)

            ret_value = alert_utility.has_stop_words(
                text,
                stop_words=stop_words
            )
            has_words = ret_value

        # get the object to apply/remove the marker interface
        obj = None
        # if it's a comment
        if getattr(self.event, 'comment', None):
            obj = self.event.comment
        # if it's a content type
        elif getattr(self.event, 'object', None):
            obj = self.event.object

        self._apply_marker_interface(obj, has_words)
        return ret_value

    @staticmethod
    def _apply_marker_interface(obj, has_stop_words):
        reindex = False
        if has_stop_words:
            alsoProvides(obj, IHasStopWords)
            reindex = True
        elif IHasStopWords.providedBy(obj):
            noLongerProvides(obj, IHasStopWords)
            reindex = True

        if reindex:
            obj.reindexObject(idxs=('object_provides', ))


class InadequateTextAlertConditionExecutor(TextAlertConditionExecutor):

    def __call__(self):
        return self.check(inadequate=True)


class ForbiddenTextAlertConditionExecutor(TextAlertConditionExecutor):

    def __call__(self):
        return self.check(forbidden=True)


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


@implementer(IInadequateTextAlertCondition, IRuleElementData)
class InadequateTextAlertCondition(TextAlertCondition):
    """"""


@implementer(IForbiddenTextAlertCondition, IRuleElementData)
class ForbiddenTextAlertCondition(TextAlertCondition):
    """"""


class TextAlertConditionAddForm(AddForm):
    schema = ITextAlertCondition
    label = _(u'Add a text alert condition')
    description = _(u'A text alert condition makes the rule apply '
                    u"only if there are stop words on the object's text.")
    form_name = _(u'Configure element')

    def create(self, data):
        condition = TextAlertCondition()
        form.applyChanges(self, condition, data)
        return condition


class TextAlertConditionAddFormView(ContentRuleFormWrapper):
    form = TextAlertConditionAddForm


class TextAlertConditionEditForm(EditForm):
    schema = ITextAlertCondition
    label = _(u'Edit a text alert condition')
    description = _(u'A text alert condition makes the rule apply '
                    u"only if there are stop words on the object's text.")
    form_name = _(u'Configure element')


class TextAlertConditionEditFormView(ContentRuleFormWrapper):
    form = TextAlertConditionEditForm


class AlertSubstitution(BaseSubstitution):

    def safe_call(self):
        text = self._get_text()
        stop_words = self._get_stop_words()

        alert_utility = getUtility(IAlert)
        return alert_utility.get_snippets(text, stop_words=stop_words)

    def _get_stop_words(self):
        return self.context.REQUEST.get('stop_words') or None

    def _get_text(self):
        raise NotImplementedError


class TextAlertSubstitution(AlertSubstitution):
    """Text alert string substitution."""
    category = _(u'All Content')
    description = _(u'Text alert snippets')

    def _get_text(self):
        if getattr(self.context, 'text', None):
            return self.context.text

        return u''


class CommentAlertSubstitution(AlertSubstitution):
    """Comment alert string substitution."""
    category = _(u'Comments')
    description = _(u'Comment alert snippets')

    def _get_text(self):
        event = self.context.REQUEST.get('event')
        if event is not None:
            return get_text_from_object(event.comment)

        return u''
