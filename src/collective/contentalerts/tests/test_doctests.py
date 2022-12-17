from collective.contentalerts.testing import (  # noqa
    COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING,
)
from collective.contentalerts.testing import optionflags
from plone.testing import layered

import doctest
import unittest


functional_tests = ("functional_contentrules.rst",)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                doctest.DocFileSuite(
                    f"tests/{test_file}",
                    package="collective.contentalerts",
                    optionflags=optionflags,
                ),
                layer=COLLECTIVE_CONTENTALERTS_FUNCTIONAL_TESTING,
            )
            for test_file in functional_tests
        ]
    )
    return suite
