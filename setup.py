"""Installer for the collective.contentalerts package."""
from setuptools import find_packages
from setuptools import setup


def read_file(filename):
    with open(filename) as file_obj:
        file_contents = file_obj.read()
    return file_contents


long_description = f"""
{read_file('README.rst')}

Contributors
============
{read_file('CONTRIBUTORS.rst')}

{read_file('CHANGES.rst')}
"""

setup(
    name="collective.contentalerts",
    version="3.2.1",
    description="An add-on for Plone to get alerts about content",
    long_description=long_description,
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Gil Forcada",
    author_email="gilforcada@gmail.com",
    url="https://github.com/collective/collective.contentalerts",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api >= 1.4.11",
        "plone.app.contentrules",
        "plone.app.contenttypes",
        "plone.app.discussion",
        "plone.app.registry",
        "plone.app.textfield",
        "plone.app.z3cform",
        "plone.contentrules",
        "plone.registry",
        "plone.stringinterp",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "setuptools",
        "six",
        "z3c.form",
        "Zope2",
        "zope.component",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.publisher",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "Acquisition",
            "plone.app.discussion",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.registry",
            "plone.testing",
            "Products.CMFPlone",
            "Products.MailHost",
            "Products.statusmessages",
            "transaction",
        ],
        "async": [
            "collective.taskqueue",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
