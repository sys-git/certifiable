#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
import six

from certifiable import CertifierTypeError, certify_int
from certifiable.cli.utils import execute_cli_command


@click.command(
    'int', help='certify an integer')
@click.option(
    '--min-value', type=int,
    help='minimum allowable value')
@click.option(
    '--max-value', type=int,
    help='maximum allowable value')
@click.argument('value', type=str)
@click.pass_obj
def cli_certify_core_integer(
    config, min_value, max_value, value,
):
    """Console script for certify_int"""

    def parser(x):
        try:
            int(x)
        except ValueError as err:
            six.raise_from(
                CertifierTypeError(
                    message='Not integer: {x}'.format(
                        x=x,
                    ),
                    value=x,
                ),
                err,
            )

    execute_cli_command(
        'integer',
        config,
        parser,
        certify_int,
        value,
        min_value=min_value,
        max_value=max_value,
        required=config['required'],
    )
