Changelog
=========

0.7 (2016-01-22)
----------------
- Monitor registry setting (stop words) for changes.
  If changes are found, verify if reviewed objects have those new stop words.
  [gforcada]

- Round of cleanups, refactorings and coverage fixes.
  [gforcada]

- Conditionally depend on collective.taskqueue to do mass processing asynchronously.
  [gforcada]

0.6 (2016-01-20)
----------------
- Apply IStopWordsVerified when discarding an alert.
  [gforcada] [staeff]

- Sort imports, use plone.api and some buildout cleanups.
  [gforcada]

0.5 (2016-01-19)
----------------
- Support Plone 4.3.7
  [gforcada]

- Make normalize a global function
  [gforcada] [staeff]

0.4.post1 (2015-08-31)
----------------------
- Add German translation.
  [staeff]

0.4.post0 (2015-08-19)
----------------------
- Create wheels as well.

0.4 (2015-08-19)
----------------
- Add a browser view to remove the IHasStopWords marker interface on a per object basis.
  [gforcada]

0.3.1 (2015-08-17)
------------------
- Make sure that the ``IHasStopWords`` marker interface is indexed on the catalog.
  [gforcada]

0.3.post0 (2015-08-15)
----------------------
- Fix package URL.
  [gforcada]

0.3 (2015-08-14)
----------------
- Correctly split stop words text so that it takes into account different line endings.
  [gforcada]

- Ignore empty lines on stop words to not produce unexpected results.
  [gforcada]

0.2 (2015-08-14)
----------------
- Split string subtitutions in two: ``text_alert`` and ``comment_alert``.
  [gforcada]

0.1 (2015-08-14)
----------------
- Initial release.
  [gforcada]

- Fix package structure:

  - remove unneeded parts
  - add travis and coveralls badges

  [gforcada]

- Add a ``plone.registry`` to keep the general stop words list.
  [gforcada]

- Add a control panel configlet to edit the stop words list.
  [gforcada]

- Add more code analysis checks, dependency tracker and MANIFEST check
  [gforcada]

- Add utility to search for stop words on a given text
  [gforcada]

- Add a plone.app.contentrules condition: ``collective.contentalerts.TextAlert``
  [gforcada]

- Add a string substitution: ``text_alert``. To be used to compose emails on a contentrule
  [gforcada]

- Apply a marker interface to the objects that are found to have a stop words.
  [gforcada]
