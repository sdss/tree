# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: utils.py
# Project: tree
# Author: Brian Cherinka
# Created: Tuesday, 17th March 2020 11:22:02 am
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Tuesday, 17th March 2020 1:41:46 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
import os
import six
from tree import Tree


def compute_changelog(new, old, pprint=None, to_list=None, remove_sas=True, include_paths=True,
                      paths_only=None):
    ''' Compute the difference between two Tree environments

    Finds and prints the difference between two tree environment
    configurations.  Accepts either string names of config files, e.g.
    "dr16" and "dr15", or the preloaded `Tree` configs, e.g.
    `Tree(config='dr16')`.  By default returns a dictionary of changes or use
    the `pprint` keyword to return a formatted print-friendly string for display.
    The `to_list` keyword returns a print-formatted list of strings parse parseable
    by `docutree` for Sphinx docs.  Set `include_paths` to True to include a changelog
    of the `sdss_access` path definitions.

    Parameters:
        new (str|Tree):
            The new tree enviroment to compare
        old (str|Tree):
            The old tree environment to compare
        pprint (bool):
            If True, returns a single joined string for printing. Default is False.
        to_list (bool):
            If True, returns a list of strings formatted for printing. Default is False.
        remove_sas (bool):
            If True, removes the SAS_BASE_DIR from environment values.  Default is True.
        include_paths (bool):
            If True, includes changes to the sdss_access PATHS section.  Default is True.
        paths_only (bool):
            If True, returns only changes in sdss_access PATHS section.  Default is False.

    Returns:
        A dictionary of relevant changes between the two releases

    Example:
        >>> # print the differences DR16 and DR15
        >>> diffs = compute_changelog('dr16', 'dr15', pprint=True)
        >>> print(diffs)
    '''

    # compute the environment changelog dictionary
    cl_dict = compute_environment_changes(new, old, remove_sas=remove_sas)

    # compute and add the paths changelog dictionary
    if include_paths or paths_only:
        path_dict = compute_path_changes(new, old, prepend_header=paths_only)
        cl_dict.update(path_dict)

    # return PATHS section only
    if paths_only:
        cl_dict = cl_dict.copy()
        cl_dict.pop('environment')
        if pprint or to_list:
            return print_paths(cl_dict, to_string=not to_list, prepend_header=paths_only)
        return cl_dict

    if pprint or to_list:
        return print_environment(cl_dict, to_string=not to_list)

    return cl_dict


def compute_environment_changes(new, old, remove_sas=True):
    ''' Compute the difference between two Tree environments

    Compares two tree environment configurations and returns a
    dictionary with keys `new`, `removed`, and `changes` indicating
    newly added environments, newly removed environments, and
    environments where environment variable definitions have changed.
    Accepts either string names of config files, e.g.
    "dr16" and "dr15", or the preloaded `Tree` configs, e.g.
    `Tree(config='dr16')`.

    Parameters:
        new (str|Tree):
            The new tree enviroment to compare
        old (str|Tree):
            The old tree environment to compare
        remove_sas (bool):
            If True, removes the SAS_BASE_DIR from environment values.  Default is True.

    Returns:
        A dictionary of relevant changes between the two releases
    '''
    dd = {'environment': {'new': {}, 'changes': {}, 'removed': {}}}

    if isinstance(new, six.string_types):
        new = Tree(config=new.lower())

    if isinstance(old, six.string_types):
        old = Tree(config=old.lower())

    new_envs = new.environ.keys()
    old_envs = old.environ.keys()
    new_name = new.environ['default']['name']
    old_name = old.environ['default']['name']
    sas = os.getenv("SAS_BASE_DIR")

    dd['releases'] = {'new': new_name, 'old': old_name}

    # find unique new enviroments
    unique_new_envs = set(new_envs) - set(old_envs)
    for env in unique_new_envs:
        dd['environment']['new'][env] = {}
        for k, v in new.environ[env].items():
            if remove_sas:
                v = v.split(sas)[-1]
            dd['environment']['new'][env][k.upper()] = v

    # find unique old enviroments
    unique_old_envs = set(old_envs) - set(new_envs)
    for env in unique_old_envs:
        dd['environment']['removed'][env] = {}
        for k, v in old.environ[env].items():
            if remove_sas:
                v = v.split(sas)[-1]
            dd['environment']['removed'][env][k.upper()] = v

    # find new or updated environment variables
    for env in new_envs:
        # skip the default
        if env == 'default' or env not in old.environ:
            continue
        uniq_vars = set(new.environ[env].keys()) - set(old.environ[env].keys())
        if not uniq_vars:
            continue

        vbase = [v.split(os.path.join(sas, new_name))[-1] for v in new.environ[env].values()]
        voldbase = [v.split(os.path.join(sas, old_name))[-1] for v in old.environ[env].values()]
        changes = set(vbase) - set(voldbase)
        if not changes:
            continue

        dd['environment']['changes'][env] = {}
        for k, v in new.environ[env].items():
            vold = old.environ[env].get(k, None)
            if vold:
                vbase = v.split(os.path.join(sas, new_name))[-1]
                voldbase = vold.split(os.path.join(sas, old_name))[-1]
                if vbase != voldbase:
                    dd['environment']['changes'][env][k.upper()] = {'from': voldbase, 'to': vbase}
            else:
                if remove_sas:
                    v = v.split(sas)[-1]
                dd['environment']['changes'][env][k.upper()] = v

    return dd


def compute_path_changes(new, old, prepend_header=None):
    ''' Compute the difference between two Tree PATH sections

    Compares two tree PATH ini sections from the given environment
    configurations and returns  adictionary with keys `new`, and `updated`,
    indicating newly added paths, and any paths that have been modified
    from the last release.  Accepts either string names of config
    files, e.g. "dr16" and "dr15", or the preloaded `Tree` configs, e.g.
    `Tree(config='dr16')`.

    Parameters:
        new (str|Tree):
            The new tree enviroment to compare
        old (str|Tree):
            The old tree environment to compare
        prepend_header (bool):
            If True, adds a header to the diff with release versions

    Returns:
        A dictionary of relevant changes between the two releases
    '''

    dd = {'paths': {'new': {}, 'updated': {}}}

    if isinstance(new, six.string_types):
        new = Tree(config=new.lower())

    if isinstance(old, six.string_types):
        old = Tree(config=old.lower())

    new_templates = new.paths
    old_templates = old.paths

    # diffs = []
    if prepend_header and 'releases' not in dd:
        new_name = new.environ['default']['name']
        old_name = old.environ['default']['name']
        dd['releases'] = {'new': new_name, 'old': old_name}

    unique_new = sorted(set(new_templates) - set(old_templates))

    if unique_new:
        for path in unique_new:
            dd['paths']['new'][path] = new_templates[path]

    # changes
    changed = []
    for name, template in new_templates.items():
        if name in old_templates and template != old_templates[name]:
            changed.append((name, template, old_templates[name]))

    if changed:
        for item in changed:
            name, newt, oldt = item
            dd['paths']['updated'][name] = {'from': oldt, 'to': newt}

    return dd


def print_environment(changes, to_string=None):
    ''' Print the environment changelog

    Formats the changelog into a print-friendly list of
    strings.

    Parameters:
        changes (dict):
            A dictionary of changes between two releases
        to_string (bool):
            If True, returns a single string

    Returns:
        A string list of print-formatted changes
    '''

    new_name = changes['releases']['new']
    old_name = changes['releases']['old']

    diffs = ['Changes: {0} from {1}'.format(new_name.upper(), old_name.upper())]
    diffs.append(' ')

    # print unique new enviroments
    for env, values in changes['environment']['new'].items():
        diffs.append('New Environment: {0}'.format(env.upper()))
        diffs.append('----------------------')
        for key, val in values.items():
            diffs.append('{0}: {1}'.format(key, val))
        diffs.append(' ')

    # print unique old enviroments
    for env, values in changes['environment']['removed'].items():
        diffs.append('Removed Environment: {0}'.format(env.upper()))
        diffs.append('----------------------')
        for key, val in values.items():
            diffs.append('{0}: {1}'.format(key, val))
        diffs.append(' ')

    # print new or updated environment variables
    for env, values in changes['environment']['changes'].items():
        diffs.append('Changes in {0}:'.format(env.upper()))
        diffs.append('----------------------')
        for key, val in values.items():
            if isinstance(val, dict):
                diffs.append('Updated {0}: {1} from {2}'.format(key, val['to'], val['from']))
            else:
                diffs.append('New {0}: {1}'.format(key, val))
        diffs.append(' ')

    if 'paths' in changes:
        diffs.append('Changes in PATHS:')
        diffs.append('-----------------')
        path_changes = print_paths(changes)
        diffs.extend(path_changes)

    if to_string:
        diffs = '\n'.join(diffs)
    return diffs


def print_paths(changes, to_string=None, prepend_header=None):
    ''' Print the path changelog

    Formats the changelog into a print-friendly list of
    strings.

    Parameters:
        changes (dict):
            A dictionary of changes between two releases
        to_string (bool):
            If True, returns a single string

    Returns:
        A string list of print-formatted changes
    '''

    diffs = []
    if prepend_header and 'releases' in changes:
        new_name = changes['releases']['new']
        old_name = changes['releases']['old']
        diffs = ['Changes: {0} from {1}'.format(new_name.upper(), old_name.upper())]
        diffs.append(' ')

    # print unique new paths
    if changes['paths']['new']:
        diffs.append('New Paths:')
        diffs.append('----------')
        for name, template in changes['paths']['new'].items():
            diffs.append('{0}: {1}'.format(name, template))

    # changes
    if changes['paths']['updated']:
        diffs.append(' ')
        diffs.append('Updated Paths:')
        diffs.append('--------------')
        for name, vals in changes['paths']['updated'].items():
            diffs.append('{0}: '.format(name))
            diffs.append('   from: {0}'.format(vals['from']))
            diffs.append('   to: {0}'.format(vals['to']))

    if to_string:
        diffs = '\n'.join(diffs)

    return diffs
