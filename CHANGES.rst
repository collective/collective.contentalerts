Changelog
=========

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
