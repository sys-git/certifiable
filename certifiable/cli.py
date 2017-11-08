#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
""" cli entry point. """

from colorama import init

from certifiable.cli_impl.common import cli
from certifiable.cli_impl.complex import add_complex_commands
from certifiable.cli_impl.core import add_core_commands

init()
add_complex_commands(cli)
add_core_commands(cli)
