#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
import sys

import click

from certifiable.cli.error_codes import OK
from certifiable.cli.utils import dump_config


@click.group()
@click.option(
    '--disable/--enable', is_flag=True, default=False,
    help='Disable certifiable')
@click.option(
    '--exit', 'ext', is_flag=True, default=False,
    help='Dump config and exit')
@click.option(
    '--required/--not-required', is_flag=True, default=False,
    help='Value is required.')
@click.option(
    '--json/--pickle', 'assume_json', is_flag=True, default=False,
    help='Assume complex types are json encoded.')
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, disable, ext, required, assume_json, verbose):
    if verbose > 2:
        click.echo('cli...')

    ctx.obj = {
        'required': required,
        'disable': disable,
        'assume_json': assume_json,
        'verbose': verbose,
    }
    if verbose > 1:
        dump_config(ctx.obj)

    if ext:
        click.echo('RESULT: NA')
        sys.exit(OK)
