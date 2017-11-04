#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click
from colorama import Back, Fore

from certifiable import certify_dict
from certifiable.cli.utils import create_certifier, execute_cli_command, load_json_pickle


@click.command('dict', help='certify a dictionary')
@click.option(
    '--schema', default=None,
    help='encoded schema to use')
@click.option(
    '--key-certifier', default=None,
    help='encoded key certifier to use')
@click.option(
    '--value-certifier', default=None,
    help='encoded value certifier to use')
@click.option(
    '--allow-extra/--no-extra', is_flag=True, default=False,
    help='allow extra keys beyond those in the schema')
@click.option(
    '--include-collections', is_flag=True, default=False,
    help='allow collections types: Mapping and MutableMapping.')
@click.argument('value', type=str)
@click.pass_obj
def cli_certify_complex_dict(
    config, schema, key_certifier, value_certifier, allow_extra,
    include_collections, value,
):
    """Console script for certify_dict."""
    verbose = config['verbose']
    if verbose:
        click.echo(Back.GREEN + Fore.BLACK + "ACTION: certify-dict")

    value = load_json_pickle(value, config)
    schema = load_json_pickle(schema, config)
    key_certifier = create_certifier(load_json_pickle(key_certifier, config))
    value_certifier = create_certifier(load_json_pickle(value_certifier, config))

    if verbose:
        if not value:
            click.echo('CERTIFY-DICT: value: \'{value}\''.format(
                value=value,
            ))
        else:
            click.echo('CERTIFY-DICT items:')
            for k, v in value.items():
                click.echo('{k} = {v}'.format(
                    k=k,
                    v=v,
                ))
        click.echo('CERTIFY-DICT: schema: {schema}'.format(
            schema=schema,
        ))
        click.echo('CERTIFY-DICT: key_certifier: {key_certifier}'.format(
            key_certifier=key_certifier,
        ))
        click.echo('CERTIFY-DICT: value_certifier: {value_certifier}'.format(
            value_certifier=value_certifier,
        ))
        click.echo('CERTIFY-DICT: allow_extra: {allow_extra}'.format(
            allow_extra=allow_extra,
        ))
        click.echo('CERTIFY-DICT: include_collections: {include_collections}'.format(
            include_collections=include_collections,
        ))

    execute_cli_command(
        'certify-dict',
        config,
        certify_dict,
        value,
        schema=schema,
        allow_extra=allow_extra,
        required=config['required'],
        key_certifier=key_certifier,
        value_certifier=value_certifier,
        include_collections=include_collections,
    )
