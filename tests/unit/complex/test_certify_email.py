#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `certifiable.complex.certify_email` method."""

import unittest
from decimal import Decimal

import mock
import six
from email_validator import EmailNotValidError

from certifiable import CertifierTypeError, CertifierValueError
from certifiable.complex import certify_email
from tests.utils import aIterable, aSet, mSet


class ComplexDictTestCase(unittest.TestCase):
    """Tests for `certifiable.complex.certify_email` method."""

    def dictUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_required(self):
        self.assertRaises(
            CertifierValueError,
            certify_email, None, required=True,
        )

    @mock.patch('certifiable.complex.email_validator.validate_email')
    def test_EmailNotValidError(self, mock_email_validator):
        mock_email_validator.side_effect = EmailNotValidError('blah')
        email_address = 'a@@b.com'
        self.assertRaises(
            CertifierValueError,
            certify_email, email_address, required=True,
        )
        mock_email_validator.assert_called_once_with(
            email_address,
            check_deliverability=False,
        )

    @mock.patch('certifiable.complex.email_validator.validate_email')
    def test_email_normalization_failure(self, mock_email_validator):
        mock_email_validator.side_effect = [{'email': 'other'}]
        email_addrss = 'a@@b.com'
        self.assertRaises(
            CertifierValueError,
            certify_email, email_addrss, required=True,
        )
        mock_email_validator.assert_called_once_with(
            email_addrss,
            check_deliverability=False,
        )

    def test_email(self):
        for i in [
            'a@b.com',
            six.u('a@b.com'),
        ]:
            self.assertEqual(certify_email(i), i)

    def test_not_str(self):
        for i in [
            list(),
            tuple(),
            aIterable,
            aSet(),
            mSet(),
            1.2,
            3,
            Decimal(4)
        ]:
            self.assertRaises(
                CertifierTypeError,
                certify_email,
                i,
                required=True,
            )


if __name__ == '__main__':
    unittest.main()
