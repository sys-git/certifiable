#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

from certifiable.cli.core.certify_int import cli_certify_core_integer


def add_core_commands(cli):
    cli.add_command(cli_certify_core_integer)
