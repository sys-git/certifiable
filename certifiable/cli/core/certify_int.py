#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
from colorama import Back, Fore

from certifiable import certify_int
from certifiable.cli.utils import execute_cli_command


@click.command(
    'int', help='certify an integer')
@click.option(
    '--min-value', type=int,
    help='minimum allowable value')
@click.option(
    '--max-value', type=int,
    help='maximum allowable value')
@click.argument('value', type=int)
@click.pass_obj
def cli_certify_core_integer(
    config, min_value, max_value, value,
):
    """Console script for certify_int"""
    verbose = config['verbose']
    if verbose:
        click.echo(Back.GREEN + Fore.BLACK + "ACTION: certify-int")

    execute_cli_command(
        'certify-int',
        config,
        certify_int,
        value,
        min_value=min_value,
        max_value=max_value,
        required=config['required'],
    )
