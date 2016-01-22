# -*- coding: utf-8 -*-
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.utilities import get_new_entries
from collective.contentalerts.utilities import verify_brain
from plone import api


def review_verified_objects(settings, event):
    """Get the new entries on settings and apply them on verified objects"""
    new_entries = get_new_entries(event.oldValue, event.newValue)

    # if there's nothing new, we are done
    if not new_entries:
        return

    new_entries = '\n'.join(new_entries)

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(object_provides=IStopWordsVerified.__identifier__)

    for brain in brains:
        verify_brain(brain, new_entries)
