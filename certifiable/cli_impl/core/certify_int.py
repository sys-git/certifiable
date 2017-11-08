#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
import six

from certifiable import CertifierTypeError, certify_int
from certifiable.cli_impl.utils import execute_cli_command, load_json_pickle


@click.command(
    'int', help='certify an integer')
@click.option(
    '--min-value', type=int,
    help='minimum allowable value')
@click.option(
    '--max-value', type=int,
    help='maximum allowable value')
@click.argument('value', type=str, nargs=-1)
@click.pass_obj
def cli_certify_core_integer(
    config, min_value, max_value, value,
):
    """Console script for certify_int"""

    def parser(v):
        # Attempt a json/pickle decode:
        try:
            v = load_json_pickle(v, config)
        except Exception:
            pass

        # Attempt a straight conversion to integer:
        try:
            return int(v)
        except Exception as err:
            six.raise_from(
                CertifierTypeError(
                    message='Not integer: {x}'.format(
                        x=v,
                    ),
                    value=v,
                ),
                err,
            )

    execute_cli_command(
        'integer',
        config,
        parser,
        certify_int,
        value[0] if value else None,
        min_value=min_value,
        max_value=max_value,
        required=config['required'],
    )
