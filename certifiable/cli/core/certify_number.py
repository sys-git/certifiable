#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
from colorama import Back, Fore

from certifiable import CertifierTypeError, certify_int
from certifiable.cli.utils import execute_cli_command


@click.command(
    'number', help='certify a number (int, float)')
@click.option(
    '--min-value', type=int,
    help='minimum allowable value')
@click.option(
    '--max-value', type=int,
    help='maximum allowable value')
@click.argument('value', type=str)
@click.pass_obj
def cli_certify_core_number(
    config, min_value, max_value, value,
):
    """Console script for certify_number"""
    verbose = config['verbose']
    if verbose:
        click.echo(Back.GREEN + Fore.BLACK + "ACTION: certify-int")

    def parser(v):
        try:
            if v.find('.') != -1:
                # Assume is float:
                v = float(v)
            else:
                # Assume is int:
                v = int(v)
        except Exception as e:
            raise CertifierTypeError(
                message='Expecting integer, got: <{value}>'.format(
                    value=value,
                ),
                required=config['required'],
                value=v,
            )
        return v

    execute_cli_command(
        'certify-int',
        config,
        parser,
        certify_int,
        value,
        min_value=min_value,
        max_value=max_value,
        required=config['required'],
    )
