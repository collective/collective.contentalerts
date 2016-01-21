# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IAlert
from collective.contentalerts.interfaces import IHasStopWords
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.utilities import get_new_entries
from collective.contentalerts.utilities import get_text_from_object
from plone import api
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


def review_verified_objects(settings, event):
    """Get the new entries on settings and apply them on verified objects"""
    new_entries = get_new_entries(event.oldValue, event.newValue)

    # if there's nothing new, we are done
    if not new_entries:
        return

    new_entries = '\n'.join(new_entries)

    catalog = api.portal.get_tool('portal_catalog')
    utility = getUtility(IAlert)

    brains = catalog(object_provides=IStopWordsVerified.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        text = get_text_from_object(obj)
        if utility.has_stop_words(text, stop_words=new_entries):
            noLongerProvides(obj, IStopWordsVerified)
            alsoProvides(obj, IHasStopWords)
            obj.reindexObject(idxs=('object_provides', ))
