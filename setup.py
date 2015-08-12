# -*- coding: utf-8 -*-
"""Installer for the collective.contentalerts package."""
from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.contentalerts',
    version='0.1',
    description="An add-on for Plone to get alerts about content",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Gil Forcada',
    author_email='gilforcada@gmail.com',
    url='http://pypi.python.org/pypi/collective.contentalerts',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.contentrules',
        'plone.app.registry',
        'plone.contentrules',
        'plone.registry',
        'Products.GenericSetup',
        'setuptools',
        'Zope2',
        'zope.component',
        # XXX migrate to z3c.form on Plone 5 (p.a.contentrules 4.0.5)
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.discussion',
            'plone.app.testing',
            'plone.browserlayer',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
