.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

========================
collective.contentalerts
========================
Get alerts whenever a (custom list of) word is found on a content object,
be that object any content type (Dexterity or Archetypes).

Can be used to:

- moderate: used as a blacklist.
- highlight: used as a whitelist.

Features
--------
- manage a list of words that will be used to search (blacklist/whitelist)
- integration with  `plone.app.contentrules`_
- standalone utility
- provide different word lists if you need them

Examples
--------
This add-on can be seen in action at the following sites:

- *Still not*

Documentation
-------------
Full documentation for end users can be found in the "docs" folder.

Translations
------------
This product has been translated into:

- *Still not*

Installation
------------
Install collective.contentalerts by adding it to your buildout::

   [buildout]

    ...

    eggs =
        collective.contentalerts


and then running "bin/buildout"

Contribute
----------
- Issue Tracker: https://github.com/collective/collective.contentalerts/issues
- Source Code: https://github.com/collective/collective.contentalerts

Support
-------
If you are having issues, please let us know.

License
-------
The project is licensed under the GPLv2.

Credits
-------

`der Freitag`_ sponsored the creation of this add-on.


.. _plone.app.contentrules:  https://pypi.python.org/pypi/plone.app.contentrules
.. _der Freitag:  https://www.freitag.de
