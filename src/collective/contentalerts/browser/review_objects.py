# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.utilities import verify_brain
from plone import api
from urllib import unquote_plus
from zope.publisher.browser import BrowserView


class ReviewObjectsView(BrowserView):

    def __call__(self):
        start = self.request('start', None)
        size = self.request('size', None)
        entries = self.request('entries', None)

        if size is None or start is None or entries is None:
            raise ValueError(
                'Missing size "{0}" or start "{1}" or entries "{2}"'.format(
                    size,
                    start,
                    entries,
                )
            )

        new_entries = unquote_plus(entries)
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            object_provides=IStopWordsVerified.__identifier__,
            sort_on='effective',
        )

        for brain in brains[start:start + size]:
            verify_brain(brain, new_entries)
