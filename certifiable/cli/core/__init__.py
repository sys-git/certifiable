#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

from certifiable.cli.core.certify_int import cli_certify_core_integer
from certifiable.cli.core.certify_number import cli_certify_core_number


def add_core_commands(cli):
    cli.add_command(cli_certify_core_integer)
    cli.add_command(cli_certify_core_number)
