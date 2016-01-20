# -*- coding: utf-8 -*-
from collective.contentalerts import _
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from plone import api
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.publisher.browser import BrowserView


class DiscardAlertView(BrowserView):

    def __call__(self):
        if IHasStopWords.providedBy(self.context):
            noLongerProvides(self.context, IHasStopWords)
            alsoProvides(self.context, IStopWordsVerified)
            self.context.reindexObject(idxs=('object_provides', ))

            api.portal.show_message(
                message=_(
                    u'stop_words_interface_removed_message',
                    default=u'The object no longer has an alert on it.'
                ),
                request=self.request,
            )

        return self.request.response.redirect(
            self.context.absolute_url(),
        )
