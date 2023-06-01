# !usr/bin/env python
# -*- coding: utf-8 -*-
#

from tree.changelog import compute_changelog, print_environment, print_paths


def test_changelog():
    cc = compute_changelog('dr17', 'dr16')

    assert cc['releases'] == {'new': 'dr17', 'old': 'dr16'}
    assert cc['environment']['new'] == {}
    assert cc['environment']['changes']['MANGA']['MANGA_AGN'] == '/dr17/manga/agn'

    assert 'apogee_astronn' in cc['paths']['new']
    assert cc['paths']['new']['apogee_astronn'] == '$APOGEE_ASTRONN/apogee_astroNN-{release}.fits'

    gema = {'from': '$MANGA_GEMA/{ver}/GEMA-{ver}.fits',
            'to': '$MANGA_GEMA/{ver}/GEMA_{ver}.fits'}
    assert cc['paths']['updated']['mangagema'] == gema


def test_change_only_paths():
    cc = compute_changelog('dr17', 'dr16', paths_only=True)
    assert cc['releases'] == {'new': 'dr17', 'old': 'dr16'}
    assert 'environment' not in cc
    assert 'apogee_astronn' in cc['paths']['new']
    assert cc['paths']['new']['apogee_astronn'] == '$APOGEE_ASTRONN/apogee_astroNN-{release}.fits'

def test_changes_newold():
    cc = compute_changelog('dr13', 'dr12')
    assert 'MANGA_SPECTRO_REDUX' in cc['environment']['new']['MANGA']
    assert 'BOSS_GALAXY_REDUX' in cc['environment']['removed']['BOSS']

def test_print_env():
    cc = compute_changelog('dr13', 'dr12')
    env = print_environment(cc)
    assert env[0] == 'Changes: DR13 from DR12'
    assert 'MANGA_SPECTRO_REDUX: /dr13/manga/spectro/redux' in env


def test_print_paths():
    cc = compute_changelog('dr17', 'dr16')
    paths = print_paths(cc)
    assert paths[0] == 'New Paths:'
    assert 'apogee_astronn: $APOGEE_ASTRONN/apogee_astroNN-{release}.fits' in paths

    paths = print_paths(cc, prepend_header=True)
    assert paths[0] == 'Changes: DR17 from DR16'