#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

from certifiable.cli_impl.complex.certify_dict import cli_certify_complex_dict


def add_complex_commands(cli):
    cli.add_command(cli_certify_complex_dict)
