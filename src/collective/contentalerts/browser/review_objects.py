# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.utilities import verify_brain
from plone import api
from urllib import unquote_plus
from zope.publisher.browser import BrowserView


class ReviewObjectsView(BrowserView):

    def __call__(self):
        start, size, entries = self._check_parameters()

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            object_provides=IStopWordsVerified.__identifier__,
            sort_on='effective',
        )

        for brain in brains[start:start + size]:
            verify_brain(brain, entries)

    def _check_parameters(self):
        start = self.request.get('start', None)
        size = self.request.get('size', None)
        entries = self.request.get('entries', None)

        msg = 'Value missing: start "{0}", size "{1}", entries "{2}"'
        for element in (start, size, entries):
            if element is None:
                raise ValueError(msg.format(start, size, entries))

        msg = 'Needs a number: start "{0}", size "{1}"'
        for element in (start, size):
            try:
                int(element)
            except ValueError:
                raise ValueError(msg.format(start, size))

        return int(start), int(size), unquote_plus(entries)
