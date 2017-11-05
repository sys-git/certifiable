#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
import json

from colorama import init

from certifiable.cli.complex import add_complex_commands
from certifiable.cli.core import add_core_commands
from common import cli

init()
add_complex_commands(cli)
add_core_commands(cli)

if __name__ == '__main__':
    cli([
        # '--exit',
        # '--verbose',
        '--verbose',
        '--disable',
        '--required',
        '--json',
        'int',
        'integer://1.2'
        # '1234.56789',
        # 'dict',
        # '',
        # 'fghjghg',
        # json.dumps({'a': 1}),
        # '--include-collections',
    ])
