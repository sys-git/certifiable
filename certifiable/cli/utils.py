#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
import json
import pickle
import sys
import traceback

import click
from colorama import Back, Fore

import certifiable
from certifiable import CertifierError, CertifierParamError, CertifierTypeError, CertifierValueError
from certifiable.cli.error_codes import CERTIFICATION_TYPE_ERROR, CERTIFICATION_VALUE_ERROR, OK


def create_certifier(config):
    """
    Config of the form:
    {
        'name': 'certify_int',
        'kwargs': dict(),
    }
    """
    if config:
        if 'name' not in config:
            sys.exit('no certifier specified')
        func_name = config['name']
        func = getattr(certifiable, func_name, None)
        if func is None:
            sys.exit('invalid certifier specified')
        certifier = func_name(
            **config.get('kwargs', {})
        )
        return certifier


def load_json_pickle(what, config):
    if what is not None:
        if config['assume_json']:
            return json.loads(what)
        return pickle.loads(what)


def dump_config(config):
    for k, v in config.items():
        click.echo(Fore.RED + Back.GREEN + 'CONFIG: {k} = {v}'.format(
            k=k,
            v=v,
        ))


def error_to_code(certifier_error):
    return {
        CertifierValueError: CERTIFICATION_VALUE_ERROR,
        CertifierTypeError: CERTIFICATION_TYPE_ERROR,
        CertifierParamError: CERTIFICATION_TYPE_ERROR,
    }[certifier_error.__class__]


def execute_cli_command(description, config, func, value, *args, **kwargs):
    verbose = config['verbose']

    if verbose:
        click.echo('{description}: value: <{value}>'.format(
            description=description.upper(),
            value=value,
        ))

    try:
        func(value, *args, **kwargs)
    except CertifierError as e:
        click.echo(Back.RED + Fore.BLACK + 'ERROR: ' + str(e))
        if verbose > 1:
            click.echo(Back.RED + Fore.BLACK + traceback.format_exc())
        sys.exit(
            error_to_code(e)
        )
    else:
        if verbose:
            click.echo(Back.GREEN + Fore.BLACK + 'RESULT: OK')
        sys.exit(OK)
