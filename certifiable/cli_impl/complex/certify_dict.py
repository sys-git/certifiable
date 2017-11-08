#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import click

from certifiable import certify_dict
from certifiable.cli_impl.utils import create_certifier, execute_cli_command, load_json_pickle


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
    '--include-collections/--exclude-collections', is_flag=True, default=False,
    help='allow collections types: Mapping and MutableMapping.')
@click.argument('value', type=str)
@click.pass_obj
def cli_certify_complex_dict(
    config, schema, key_certifier, value_certifier, allow_extra,
    include_collections, value,
):
    """Console script for certify_dict."""
    schema = load_json_pickle(schema, config)
    key_certifier = create_certifier(load_json_pickle(key_certifier, config))
    value_certifier = create_certifier(load_json_pickle(value_certifier, config))

    execute_cli_command(
        'dict',
        config,
        lambda x: load_json_pickle(x, config),
        certify_dict,
        value,
        allow_extra=allow_extra,
        include_collections=include_collections,
        key_certifier=key_certifier,
        required=config['required'],
        schema=schema,
        value_certifier=value_certifier,
    )
