# -*- coding: utf-8 -*-
from collective.contentalerts import ASYNC
from collective.contentalerts import logger
from collective.contentalerts.interfaces import IStopWordsVerified
from collective.contentalerts.utilities import get_new_entries
from collective.contentalerts.utilities import verify_brain
from plone import api


if ASYNC:
    from collective.taskqueue import taskqueue


def review_verified_objects(settings, event):
    """Get the new entries on settings and apply them on verified objects"""
    new_entries = get_new_entries(event.oldValue, event.newValue)

    # if there's nothing new, we are done
    if not new_entries:
        return

    new_entries = '\n'.join(new_entries)

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(object_provides=IStopWordsVerified.__identifier__)

    if not ASYNC:
        for brain in brains:
            verify_brain(brain, new_entries)
    else:
        # split the work to review the verified objects for new stop words in
        # batches
        batch = 1
        amount = 300
        count = len(brains)
        while count > 0:
            view_path = '/{0}/@@review-objects'.format(
                api.portal.get().id
            )
            params = {
                'start': amount * batch - amount,
                'size': amount,
                'entries': new_entries,
            }
            logger.warn('Queued request {0} {1}'.format(view_path, params))
            taskqueue.add(
                view_path,
                params=params
            )

            batch += 1
            count -= amount
