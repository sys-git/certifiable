#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
import six
from colorama import Back, Fore

from certifiable import CertifierTypeError
from certifiable.cli_impl.utils import execute_cli_command, load_json_pickle
from certifiable.core import certify_number


@click.command(
    'number', help='certify a number (int, float)')
@click.option(
    '--min-value', type=int,
    help='minimum allowable value')
@click.option(
    '--max-value', type=int,
    help='maximum allowable value')
@click.argument('value', type=str, nargs=-1)
@click.pass_obj
def cli_certify_core_number(
    config, min_value, max_value, value,
):
    """Console script for certify_number"""
    verbose = config['verbose']
    if verbose:
        click.echo(Back.GREEN + Fore.BLACK + "ACTION: certify-int")

    def parser(v):
        # Attempt a json/pickle decode:
        try:
            v = load_json_pickle(v, config)
        except Exception:
            pass

        # Attempt a straight conversion to float or integer:
        try:
            if v.find('.') != -1:
                # Assume is float:
                v = float(v)
            else:
                # Assume is int:
                v = int(v)
            return v
        except Exception as err:
            six.raise_from(
                CertifierTypeError(
                    message='Not integer or float: {v}'.format(
                        v=v,
                    ),
                    value=v,
                ),
                err,
            )

    execute_cli_command(
        'number',
        config,
        parser,
        certify_number,
        value[0] if value else None,
        min_value=min_value,
        max_value=max_value,
        required=config['required'],
    )
