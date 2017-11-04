#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

"""

THIS WORKS

"""
import click


@click.command('x', help='help for command x')
@click.option('--count', default=1, help='Number of greetings.')
@click.pass_obj
def x(obj, count):
    click.echo('obj: %s!' % obj)
    click.echo('count: %s!' % count)


def init_commands(group):
    group.add_command(x)


@click.group()
@click.option('--x', default=10, help='Number for x.')
@click.pass_context
def entry_point(ctx, x):
    click.echo('entry point...')
    click.echo('x: %s!' % x)

    ctx.obj = {
        'a': 1,
        'x': x,
    }


init_commands(entry_point)

if __name__ == '__main__':
    entry_point(['x', '--count=222'])
