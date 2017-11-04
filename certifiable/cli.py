# -*- coding: utf-8 -*-

"""Console script for certifiable."""
import json
import sys

import click

import certifiable
from certifiable import certify_dict, enable


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


def init(args):
    @click.command('dict')
    @click.pass_obj
    @click.option(
        '--json-schema', default=None,
        help='json encoded schema to use')
    @click.option(
        '--json-dict', default=None,
        help='json encoded dict to validate')
    @click.option(
        '--json-key-certifier', default=None,
        help='json encoded key certifier to use')
    @click.option(
        '--json-value-certifier', default=None,
        help='json encoded value certifier to use')
    @click.option(
        '--allow-extra', default=False,
        help='allow extra keys beyond those in the schema')
    @click.option(
        '--include-collections', default=False,
        help='allow collections types: Mapping and MutableMapping')
    def cli_certify_complex_dict(
        config, json_schema, json_dict, json_key_certifier, json_value_certifier, allow_extra,
        include_collections,
    ):
        """Console script for certifiable."""
        click.echo("certifying dict...")
        key_certifier = create_certifier(
            json.loads(json_key_certifier) if json_key_certifier else None)
        value_certifier = create_certifier(
            json.loads(json_value_certifier) if json_value_certifier else None)

        certify_dict(
            json.loads(json_dict) if json_dict else None,
            schema=json.loads(json_schema) if json_schema else None,
            allow_extra=allow_extra,
            required=config['required'],
            key_certifier=key_certifier,
            value_certifier=value_certifier,
            include_collections=include_collections)

    @click.group(
        name='certifiable')
    @click.option(
        '--disable', type=bool, default=False,
        help='Disable certifiable')
    @click.option(
        '--ext', type=bool, default=False,
        help='Dump config and exit')
    @click.option(
        '--required', default=False,
        help='The value is required to be non-None')
    @click.pass_context
    def run(ctx, disable, ext, required):
        ctx.object = {
            'enable': not disable,
            'required': required,
        }
        if ext:
            print(ctx.object)
            sys.exit(0)
        enable(not disable)

    group = run
    group.add_command(cli_certify_complex_dict)

    run(args)


def main():
    init(['dict'])


if __name__ == "__main__":
    main()
