# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IHasStopWords
from zope.interface import noLongerProvides
from zope.publisher.browser import BrowserView


class DiscardAlertView(BrowserView):

    def __call__(self):
        if IHasStopWords.providedBy(self.context):
            noLongerProvides(self.context, IHasStopWords)
            self.context.reindexObject(idxs=('object_provides', ))

        return self.request.response.redirect(
            self.context.absolute_url(),
        )
