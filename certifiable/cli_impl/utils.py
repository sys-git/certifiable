#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import datetime
import json
import pickle
import sys
import time
import traceback
from decimal import Decimal

import click
import maya
import six
from colorama import Back, Fore
from maya import MayaDT
from six.moves import urllib

import certifiable
from certifiable import CertifierError, CertifierParamError, CertifierTypeError, \
    CertifierValueError, enable
from certifiable.cli_impl.error_codes import CERTIFICATION_TYPE_ERROR, CERTIFICATION_VALUE_ERROR, OK


def create_certifier(config):
    if config:
        if 'name' not in config:
            sys.exit('no certifier specified')
        func_name = config['name']
        func = getattr(
            certifiable,
            func_name,
            None,
        )
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
        click.echo(
            Fore.RED +
            Back.GREEN +
            'CONFIG: {k} = {v}'.format(
                k=k,
                v=v,
            ))


def error_to_code(certifier_error):
    if certifier_error is None:
        return OK

    return {
        CertifierValueError: CERTIFICATION_VALUE_ERROR,
        CertifierTypeError: CERTIFICATION_TYPE_ERROR,
        CertifierParamError: CERTIFICATION_TYPE_ERROR,
    }[certifier_error.__class__]


def load_value_from_schema(v):
    """
    Load a value from a schema defined string.
    """
    x = urllib.parse.urlparse(v)

    if x.scheme.lower() == 'decimal':
        v = Decimal(x.netloc)
    elif x.scheme.lower() in ['int', 'integer']:
        v = int(x.netloc)
    elif x.scheme.lower() == 'float':
        v = float(x.netloc)
    elif x.scheme.lower() in ['s', 'str', 'string']:
        v = str(x.netloc)
    elif x.scheme.lower() in ['u', 'unicode']:
        v = six.u(x.netloc)
    elif x.scheme.lower() == 'email':
        v = six.u(x.netloc)
    elif x.scheme.lower() == 'bool':
        v = bool(x.netloc)
    elif x.scheme.lower() in ['b', 'bytes']:
        v = six.b(x.netloc)
    elif x.scheme.lower() in ['ts.iso8601', 'timestamp.iso8601']:
        v = MayaDT.from_iso8601(x.netloc).datetime()
    elif x.scheme.lower() in ['ts.rfc2822', 'timestamp.rfc2822']:
        v = MayaDT.from_rfc2822(x.netloc).datetime()
    elif x.scheme.lower() in ['ts.rfc3339', 'timestamp.rfx3339']:
        v = MayaDT.from_rfc3339(x.netloc).datetime()
    elif x.scheme.lower() in ['ts', 'timestamp']:
        v = maya.parse(x.netloc).datetime()
    elif x.scheme.lower() == 'date':
        v = datetime.date.fromtimestamp(float(x.netloc))
    elif x.scheme.lower() == 'time':
        v = time.gmtime(float(x.netloc))
    else:
        v = None

    return v


def parse_value(v, parser, config, description):
    """
    Convert a string received on the command-line into
    a value or None.

    :param str v:
        The value to parse.
    :param parser:
        The fallback callable to load the value if loading
        from scheme fails.
    :param dict config:
        The config to use.
    :param str description:
        Description (for debugging)
    :return:
        The parsed value
    :rtype:
        object
    """
    val = None

    if v == '':
        return

    if v is not None:
        try:
            val = load_value_from_schema(v)
        except Exception as e:
            six.raise_from(
                CertifierTypeError(
                    message='{kind}'.format(
                        description=description,
                        kind=type(v).__name__,
                    ),
                    required=config['required'],
                    value=v,
                ),
                e)
        else:
            if val is None:
                try:
                    return parser(v)
                except CertifierTypeError:
                    raise
                except CertifierValueError:
                    raise
                except TypeError as e:
                    six.raise_from(
                        CertifierTypeError(
                            message='{kind}'.format(
                                description=description,
                                kind=type(v).__name__,
                            ),
                            required=config['required'],
                            value=v,
                        ),
                        e)
                except ValueError as e:
                    six.raise_from(
                        CertifierValueError(
                            message='{value}'.format(
                                description=description,
                                value=v,
                            ),
                            required=config['required'],
                            value=v,
                        ),
                        e)

    return val


def execute_cli_command(
    description, config, parser, func, value, *args, **kwargs
):
    verbose = config['verbose']
    if verbose:
        click.echo(
            Back.GREEN +
            Fore.BLACK +
            "ACTION: KIND: {d}".format(
                d=description,
            ))

    # Enabled/Disable certifiable:
    enable(enabler=not config['disable'])

    err = None
    try:
        # All values comes in as a string which need decoding.
        value = parse_value(value, parser, config, description)

        if verbose:
            click.echo('{description}: KIND: {kind}, VALUE: {value}'.format(
                description=description.upper(),
                kind=type(value).__name__,
                value=value,
            ))
        if verbose:
            for k, v in sorted(kwargs.items()):
                click.echo('{description} OPTS: {k} = {v}'.format(
                    description=description.upper(),
                    k=k,
                    v=v,
                ))
        # Execute the core/complex certifier:
        func(value, *args, **kwargs)
    except CertifierValueError as err:
        click.echo(
            Back.RED +
            Fore.BLACK +
            'RESULT: ERROR: VALUE: ' +
            str(err),
        )
        if verbose > 1:
            click.echo(
                Back.RED +
                Fore.BLACK +
                traceback.format_exc(),
            )
    except CertifierTypeError as err:
        click.echo(
            Back.RED +
            Fore.BLACK +
            'RESULT: ERROR: KIND: ' +
            str(err),
        )
        if verbose > 1:
            click.echo(
                Back.RED +
                Fore.BLACK +
                traceback.format_exc(),
            )
    except CertifierError as err:  # pragma: no cover
        click.echo(
            Back.RED +
            Fore.BLACK +
            'RESULT: ERROR: ' +
            str(err),
        )
        if verbose > 1:
            click.echo(
                Back.RED +
                Fore.BLACK +
                traceback.format_exc(),
            )
    else:
        if verbose:
            click.echo(
                Back.GREEN +
                Fore.BLACK +
                'RESULT: OK',
            )

    sys.exit(
        error_to_code(err)
    )
