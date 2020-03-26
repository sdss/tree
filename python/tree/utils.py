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


def compute_changelog(new, old, pprint=None, remove_sas=True):
    ''' Compute the difference between two Tree environments
    
    Finds and prints the difference between two tree environment
    configurations.  Accepts either string names of config files, e.g. 
    "dr16" and "dr15", or the preloaded `Tree` configs, e.g. 
    `Tree(config='dr16')`.

    Parameters:
        new (str|Tree):
            The new tree enviroment to compare
        old (str|Tree):
            The old tree environment to compare
        pprint (bool):
            If True, returns a single joined string for printing
        remove_sas (bool):
            If True, removes the SAS_BASE_DIR from environment values.  Default is True.
    
    Returns:
        A list of strings with printed changes

    Example:
        >>> # print the differences DR16 and DR15
        >>> diffs = compute_changelog('dr16', 'dr15', pprint=True)
        >>> print(diffs)
    '''

    if isinstance(new, six.string_types):
        new = Tree(config=new.lower())

    if isinstance(old, six.string_types):
        old = Tree(config=old.lower())

    new_envs = new.environ.keys()
    old_envs = old.environ.keys()
    new_name = new.environ['default']['name']
    old_name = old.environ['default']['name']
    sas = os.getenv("SAS_BASE_DIR")

    diffs = ['Changes: {0} from {1}'.format(new_name.upper(), old_name.upper())]
    diffs.append(' ')

    # find unique new enviroments
    unique_new_envs = set(new_envs) - set(old_envs)
    for env in unique_new_envs:
        diffs.append('New Enviroment: {0}'.format(env.upper()))
        diffs.append('----------------------')
        for k, v in new.environ[env].items():
            if remove_sas:
                v = v.split(sas)[-1]
            diffs.append('{0}: {1}'.format(k.upper(), v))
        diffs.append(' ')

    # find unique old enviroments
    unique_old_envs = set(old_envs) - set(new_envs)
    for env in unique_old_envs:
        diffs.append('Removed Enviroment: {0}'.format(env.upper()))
        diffs.append('----------------------')
        for k, v in old.environ[env].items():
            if remove_sas:
                v = v.split(sas)[-1]
            diffs.append('{0}: {1}'.format(k.upper(), v))
        diffs.append(' ')

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

        diffs.append('Changes in {0}:'.format(env.upper()))
        diffs.append('----------------------')
        for k, v in new.environ[env].items():
            vold = old.environ[env].get(k, None)
            if vold:
                vbase = v.split(os.path.join(sas, new_name))[-1]
                voldbase = vold.split(os.path.join(sas, old_name))[-1]
                if vbase != voldbase:
                    diffs.append('Updated {0}: {1} from {2}'.format(k.upper(), vbase, voldbase))
            else:
                if remove_sas:
                    v = v.split(sas)[-1]
                diffs.append('New {0}: {1}'.format(k.upper(), v))
        diffs.append(' ')

    if pprint:
        diffs = '\n'.join(diffs)
    return diffs
