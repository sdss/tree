# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-11-30 12:19:16
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-01 16:11:33

from __future__ import print_function, division, absolute_import
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils import statemachine
import traceback

# This file is a basic example of how to write a Sphinx plugin to document
# custom data.


def _indent(text, level=1):
    ''' Does a proper indenting for Sphinx rst '''

    prefix = ' ' * (4 * level)

    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if line.strip() else line)

    return ''.join(prefixed_lines())


def _format_command(name, envvars, base=None):
    ''' Creates a list-table directive

    for a set of defined environment variables

    Parameters:
        name (str):
            The name of the config section
        envvars (dict):
            A dictionary of the environment variable definitions from the config
        base (str):
            The SAS_BASE to remove from the filepaths

    Yields:
        A string rst-formated list-table directive

    '''

    yield '.. list-table:: {0}'.format(name)
    yield _indent(':widths: 20 50')
    yield _indent(':header-rows: 1')
    yield ''
    yield _indent('* - Name')
    yield _indent('  - Path')
    for envvar, path in envvars.items():
        tail = path.split(base)[1] if base and base in path else path
        tail = envvar.upper() if envvar.upper() == 'SAS_BASE_DIR' else tail
        yield _indent('* - {0}'.format(envvar.upper()))
        yield _indent('  - {0}'.format(tail))
    yield ''


class TreeDirective(rst.Directive):
    ''' The directive which instructs Sphinx how to format the Tree config documentation '''

    has_content = False
    required_arguments = 1
    option_spec = {
        'prog': directives.unchanged_required,
        'title': directives.unchanged,
        'remove-sasbase': directives.flag,
    }

    def _load_module(self, module_path):
        """Load the module."""

        # __import__ will fail on unicode,
        # so we ensure module path is a string here.
        module_path = str(module_path)

        try:
            module_name, attr_name = module_path.split(':', 1)
        except ValueError:  # noqa
            raise self.error('"{0}" is not of format "module:parser"'.format(module_path))

        try:
            mod = __import__(module_name, globals(), locals(), [attr_name])
        except (Exception, SystemExit) as exc:  # noqa
            err_msg = 'Failed to import "{0}" from "{1}". '.format(attr_name, module_name)
            if isinstance(exc, SystemExit):
                err_msg += 'The module appeared to call sys.exit()'
            else:
                err_msg += 'The following exception was raised:\n{0}'.format(traceback.format_exc())

            raise self.error(err_msg)

        if not hasattr(mod, attr_name):
            raise self.error('Module "{0}" has no attribute "{1}"'.format(module_name, attr_name))

        return getattr(mod, attr_name)

    def _generate_section(self, name, config, cfg_section='default', remove_sasbase=False):
        """Generate the relevant Sphinx nodes.

        Generates a section for the Tree datamodel.  Formats a tree section
        as a list-table directive.

        Parameters:
            name (str):
                The name of the config to be documented, e.g. 'sdsswork'
            config (dict):
                The tree dictionary of the loaded config environ
            cfg_section (str):
                The section of the config to load
            remove_sasbase (bool):
                If True, removes the SAS_BASE_DIR from the beginning of each path

        Returns:
            A section docutil node

        """

        # the source name
        source_name = name

        # Title
        section = nodes.section(
            '',
            nodes.title(text=cfg_section),
            ids=[nodes.make_id(cfg_section)],
            names=[nodes.fully_normalize_name(cfg_section)])

        # Summarize
        result = statemachine.ViewList()
        base = config['default']['filesystem'] if remove_sasbase else None
        lines = _format_command(cfg_section, config[cfg_section], base=base)
        for line in lines:
            result.append(line, source_name)

        self.state.nested_parse(result, 0, section)

        return [section]

    def run(self):
        self.env = self.state.document.settings.env

        command = self._load_module(self.arguments[0])

        if 'prog' in self.options:
            prog_name = self.options.get('prog')
        else:
            raise self.error(':prog: must be specified')

        # get instance and config
        instance = command(config=prog_name)
        config = instance.environ

        # get options
        remove_sasbase = 'remove-sasbase' in self.options

        # add a new section for each config part
        sections = []
        for cfg_section, envars in config.items():
            if cfg_section != 'default':
                sections.extend(self._generate_section(prog_name, config, cfg_section=cfg_section,
                                remove_sasbase=remove_sasbase))
        return sections


def setup(app):
    app.add_directive('datamodel', TreeDirective)



