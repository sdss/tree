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
import importlib
import re

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


def _format_changelog(changes):
    ''' Format a changelog for a Tree '''

    yield '.. role:: maroon'

    # check if changelog has a PATHS section
    has_paths = 'Changes in PATHS:' in changes
    if has_paths:
        path_idx = changes.index('Changes in PATHS:')
        path_changes = changes[path_idx:]
        changes = changes[:path_idx]

    # yield lines from the Environment section
    for line in changes:
        if 'Environment' in line or 'Changes' in line:
            yield f'**{line}**'
        elif re.search('[a-z]', line):
            new = re.sub(r'(New\s|Updated\s|^)(.*?):', r'\1:maroon:`\2`:', line)
            yield '* ' + new
        yield ''

    # yield lines from the PATHS section
    if has_paths:
        # list mode
        for line in path_changes:
            if 'Changes' in line:
                yield f'**{line}**'
                yield ''
            elif 'New' in line or 'Updated' in line:
                yield '* ' + _indent(f'**{line.strip()}**')
            elif re.search('[a-z]', line):
                # nested list From To
                if line.strip().startswith(('from', 'to')):
                    line = line.replace('to:', '**To:**').replace('from:', '**From:**')
                    yield _indent('    * ' + line, level=2)
                else:
                    name, template = line.split(':', 1)
                    yield _indent(f'    * :maroon:`{name}`: {template}')


def load_module(module_path, error=None, products=None):
    """Load the module."""

    # Exception to raise
    error = error if error else RuntimeError

    # __import__ will fail on unicode,
    # so we ensure module path is a string here.
    module_path = str(module_path)
    try:
        module_name, attr_name = module_path.split(':', 1)
    except ValueError:  # noqa
        raise error('"{0}" is not of format "module:object"'.format(module_path))

    # import the module
    try:
        mod = importlib.import_module(module_name)
    except (Exception, SystemExit) as exc:
        err_msg = 'Failed to import module "{0}". '.format(module_name)
        if isinstance(exc, SystemExit):
            err_msg += 'The module appeared to call sys.exit()'
        else:
            err_msg += 'The following exception was raised:\n{0}'.format(
                traceback.format_exc())

        raise error(err_msg)

    # check what kind of module
    if products:
        module = mod.dm.products
    else:
        module = mod

    if not hasattr(module, attr_name):
        raise error('Module "{0}" has no attribute "{1}"'.format(module_name, attr_name))

    return getattr(module, attr_name)


class TreeDirective(rst.Directive):
    ''' The directive which instructs Sphinx how to format the Tree config documentation '''

    has_content = False
    required_arguments = 1
    option_spec = {
        'prog': directives.unchanged_required,
        'title': directives.unchanged,
        'remove-sasbase': directives.flag,
    }

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
        base = config['default']['FILESYSTEM'] if remove_sasbase else None
        lines = _format_command(cfg_section, config[cfg_section], base=base)
        for line in lines:
            result.append(line, source_name)

        self.state.nested_parse(result, 0, section)

        return [section]

    def run(self):
        self.env = self.state.document.settings.env

        command = load_module(self.arguments[0])

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


class TreeChangeDirective(rst.Directive):
    has_content = False
    required_arguments = 1
    option_spec = {
        'prog': directives.unchanged_required,
        'title': directives.unchanged,
        'drs': directives.unchanged_required,
        'remove-sasbase': directives.flag,
    }

    def run(self):
        self.env = self.state.document.settings.env

        command = load_module(self.arguments[0])

        if 'prog' in self.options:
            prog_name = self.options.get('prog')
        else:
            raise self.error(':prog: must be specified')

        # get options
        remove_sasbase = 'remove-sasbase' in self.options

        # get drs
        drs = self.options.get('drs')
        new, old = drs.replace(' ', '').split(',')

        # compute and format the changelog lines
        lines = command(new, old, remove_sas=remove_sasbase, to_list=True)
        title = lines[0]
        lines = lines[1:]
        lines = _format_changelog(lines)

        # the source name
        source_name = title

        # Title
        section = nodes.section(
            '',
            nodes.title(text=source_name),
            ids=[nodes.make_id(source_name)],
            names=[nodes.fully_normalize_name(source_name)])

        result = statemachine.ViewList()
        for line in lines:
            result.append(line, source_name)

        self.state.nested_parse(result, 0, section)

        return [section]


def setup(app):
    app.add_directive('datamodel', TreeDirective)
    app.add_directive('changelog', TreeChangeDirective)



