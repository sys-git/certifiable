#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

"""Tests for `certifiable.certify_int` via `certifiable.cli`."""
import json
import unittest

import mock
from click.testing import CliRunner

import certifiable
from certifiable.cli_impl.error_codes import CERTIFICATION_TYPE_ERROR, CERTIFICATION_VALUE_ERROR, OK


class CliTestCase(unittest.TestCase):
    """Tests for `certifiable` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    """ common """

    def test_no_params(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(certifiable.cli.cli)
        assert result.exit_code == OK
        help_result = runner.invoke(certifiable.cli.cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_certify_non_int(self):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                'int',
                'i am the one and only',
            ],
        )
        assert result.exit_code == CERTIFICATION_TYPE_ERROR

    def test_certify_int_using_scheme(self):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                'int',
                'int://123',
            ],
        )
        assert result.exit_code == OK

    @mock.patch('certifiable.utils.exec_func')
    def test_certify_int(self, mock_exec_func):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                'int',
                '123',
            ],
        )
        assert result.exit_code == OK
        mock_exec_func.assert_called_once()
        call = mock_exec_func.call_args_list[0].call_list()[0]
        assert call[0][1] == 123
        assert call[1] == dict(
            min_value=None,
            max_value=None,
            required=True,
        )

    def test_certify_int_no_value_given(self):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                'int',
            ],
        )
        assert result.exit_code == CERTIFICATION_VALUE_ERROR

    @mock.patch('certifiable.utils.exec_func')
    def test_certify_int_not_required_no_value_given(self, mock_exec_func):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                '--not-required',
                'int',
            ],
        )
        assert result.exit_code == OK
        mock_exec_func.assert_called_once()
        call = mock_exec_func.call_args_list[0].call_list()[0]
        assert call[0][1] is None
        assert call[1] == dict(
            min_value=None,
            max_value=None,
            required=False,
        )

    @mock.patch('certifiable.utils.exec_func')
    def test_certify_int_not_required_value_given(self, mock_exec_func):
        value = 123
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                '--not-required',
                'int',
                str(value),
            ],
        )
        assert result.exit_code == OK
        mock_exec_func.assert_called_once()
        call = mock_exec_func.call_args_list[0].call_list()[0]
        assert call[0][1] == value
        assert call[1] == dict(
            min_value=None,
            max_value=None,
            required=False,
        )

    """ specific to int """

    @mock.patch('certifiable.utils.exec_func')
    def test_certify_int_bounds_checked(self, mock_exec_func):
        value = 123
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--verbose',
                '--verbose',
                'int',
                str(value),
                '--min-value',
                '-10',
                '--max-value',
                '200',
            ],
        )
        assert result.exit_code == OK
        mock_exec_func.assert_called_once()
        call = mock_exec_func.call_args_list[0].call_list()[0]
        assert call[0][1] == value
        assert call[1] == dict(
            min_value=-10,
            max_value=200,
            required=True,
        )

    def test_certify_int_bounds_checked_min_value_fails(self):
        runner = CliRunner()
        v = '"{x}"'.format(
            x=json.dumps(-11))
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                '--json',
                'int',
                '--min-value',
                '-10',
                '--max-value',
                '200',
                v,
            ],
        )
        assert result.exit_code == CERTIFICATION_VALUE_ERROR
        assert result.output == u'RESULT: ERROR: VALUE: -11 is less than minimum acceptable -10\n'

    def test_certify_int_bounds_checked_max_value_fails(self):
        runner = CliRunner()
        result = runner.invoke(
            certifiable.cli.cli,
            args=[
                'int',
                '--min-value',
                '-10',
                '--max-value',
                '200',
                '201',
            ],
        )
        assert result.exit_code == CERTIFICATION_VALUE_ERROR
        assert result.output == u'RESULT: ERROR: VALUE: 201 is more than the maximum acceptable ' \
                                u'200\n'


if __name__ == '__main__':
    unittest.main()
