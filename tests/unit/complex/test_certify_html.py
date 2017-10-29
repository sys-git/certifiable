#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `certifiable.complex.certify_html` method."""

import unittest

import six

from certifiable import CertifierTypeError
# from certifiable.complex import certify_html
from tests.utils import aSequence, aSet, mSequence, mSet


@unittest.skip
class ComplexHtmlTestCase(unittest.TestCase):
    """Tests for `certifiable.complex.certify_html` method."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_type(self):
        html_source = 'TODO: SOme valid html'

        for i in [
            six.b(html_source),
        ]:
            certify_html(
                i,
            )

    def test_not_type(self):
        for i in [
            1,
            object(),
            mSequence(),
            aSequence(),
            aSet(),
            mSet(),
            '',
        ]:
            print(i)
            self.assertRaises(
                CertifierTypeError,
                certify_html,
                i,
                required=False,
            )


if __name__ == '__main__':
    unittest.main()
