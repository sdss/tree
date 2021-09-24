
.. _changes:

Changes in the Tree
===================

The definitions of many SDSS environment variables and ``sdss_access`` path names 
can change over time, as directory paths or file locations change as data gets shuffled around, or
items get prepared for public release.  ``sdss-tree`` provides a few convenience functions for 
tracking and identifying these changes across different SDSS data releases, or more specifically, 
across the different ``sdss-tree`` configurations.  

View the history of a single parameter
--------------------------------------

To lookup the definition of a single environment variable or ``sdss_access`` path name, use 
the `~tree.tree.get_envvar_history` or `~tree.tree.get_path_history` convenience functions.  These
functions returns a dictionary of ``tree configurations`` with the value of the specified 
environment variable or ``sdss_access`` path name.

For example, to lookup all available defintions for the ``MANGA_HI`` environment variable, do
::

    >>> from tree.tree import get_envvar_history, get_path_history

    >>> # return all available definitions for the MANGA_HI environment variable
    >>> get_envvar_history('MANGA_HI')
    {'bosswork': None,
     'mpl3': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl4': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl5': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl6': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl7': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl8': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl9': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl10': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'mpl11': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI',
     'dr7': None,
     'dr8': None,
     'dr9': None,
     'dr10': None,
     'dr11': None,
     'dr12': None,
     'dr13': None,
     'dr14': None,
     'dr15': '/Users/Brian/Work/sdss/sas/dr15/manga/HI',
     'dr16': '/Users/Brian/Work/sdss/sas/dr16/manga/HI',
     'dr17': '/Users/Brian/Work/sdss/sas/dr17/manga/HI',
     'sdss5': None,
     'sdsswork': '/Users/Brian/Work/sdss/sas/mangawork/manga/HI'}

For example, to lookup all available defintions for the ``mangaimage`` access path name, do
::

    >>> from tree.tree import get_path_history

    >>> # return all available definitions for the mangaimage access path name
    >>> get_path_history('mangaimage')
    {'bosswork': None,
     'mpl3': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'mpl4': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'mpl5': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'mpl6': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'mpl7': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'mpl8': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png',
     'mpl9': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png',
     'mpl10': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png',
     'mpl11': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png',
     'dr7': None,
     'dr8': None,
     'dr9': None,
     'dr10': None,
     'dr11': None,
     'dr12': None,
     'dr13': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'dr14': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'dr15': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'dr16': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/{dir3d}/images/{ifu}.png',
     'dr17': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png',
     'sdss5': None,
     'sdsswork': '$MANGA_SPECTRO_REDUX/{drpver}/{plate}/images/{ifu}.png'}

Compute a complete changelog
----------------------------

To compute a complete changelog for all environment variables and ``sdss_access`` path names, 
across all releases, i.e. ``tree`` configurations, use the `~tree.changeloge.compute_changelog` 
function.  ``compute_changelog`` returns a dictionary of changes in the ``environment``, or ``paths``
sections of the ``Tree``, categorized as ``new``, ``updated``, or ``removed`` definitions.  

To compute the changelog between DR17 and DR16
::

    >>> from tree.changeloge import compute_changelog
    >>> cl = compute_changelog('dr17', 'dr16')

    >>> # show the envvar changes
    >>> cl['environment']
    {'new': {},
     'changes': {'SDSS': {'SDSS_QSO': '/dr17/sdss/qso/dr7_qsoals'},
      'APOGEE': {'APOGEE_FIRE_SIM': '/dr17/apogee/apogee/vac/apogee-fire_sim',
      'APOGEE_GC': '/dr17/apogee/apogee/vac/apogee-gc',
      'APOGEE_NC': '/dr17/apogee/apogee/vac/apogee-nc',
      'APOGEE_NET': '/dr17/apogee/apogee/vac/apogee-net',
      'APOGEE_PHOTVAR': '/dr17/apogee/apogee/vac/apogee-photvar',
      'APOGEE_SB2': '/dr17/apogee/apogee/vac/apogee-sb2',
      'APOGEE_WD_BINARY': '/dr17/apogee/apogee/vac/apogee-wd_binary',
      'APOGEE_DISTMASS': '/dr17/apogee/apogee/vac/apogee-distmass',
      'APOGEE_GRAVPOT16': '/dr17/apogee/apogee/vac/apogee-gravpot16'},
      'MANGA': {'MANGAPREIM_DIR': {'from': '$PRODUCT_ROOT/data/manga/mangapreim/tags/v2_5',
        'to': '$PRODUCT_ROOT/data/manga/mangapreim/tags/v2_9'},
      'MANGACORE_DIR': {'from': '$PRODUCT_ROOT/repo/manga/mangacore/tags/v1_6_2',
        'to': '$PRODUCT_ROOT/repo/manga/mangacore/tags/v1_9_1'},
      'MANGA_AGN': '/dr17/manga/agn',
      'MANGA_MANDALA': '/dr17/manga/mandala',
      'MANGA_SPECTRO_LENSING': '/dr17/manga/spectro/lensing',
      'MANGA_SPECZ': '/dr17/manga/spectro/specz'}},
    'removed': {}}

    >>> # show the path changes
    >>> cl['paths']
    {'new': {'apogee_astronn': '$APOGEE_ASTRONN/apogee_astroNN-{release}.fits',
      'apogee_distmass': '$APOGEE_DISTMASS/APOGEE_DistMass-{version}.fits',
      'apogee_fire_sim': '$APOGEE_FIRE_SIM/{firesimver}/{simulation}/lsr_{lsr}/apogee-{simulation}-lsr-{lsr}-rslice-{slice}.fits',
      'apogee_gc': '$APOGEE_GC/GC_{type}_VAC-{gcver}.fits',
      'apogee_gravpot16': '$APOGEE_GRAVPOT16/GravPot16_VAC_DR17.fits',
      'apogee_nc_abund': '$APOGEE_NC/{release}_nc_abund_{version}.fits',
      'apogee_net_II': '$APOGEE_NET/apogee_net_II-{version}.fits',
      'apogee_occam_cluster': '$APOGEE_OCCAM/occam_cluster-DR17.fits',
      'apogee_occam_member': '$APOGEE_OCCAM/occam_member-DR17.fits',
      'apogee_photvar': '$APOGEE_PHOTVAR/{version}/APOGEE-PhotVar-{version}.fits',
      ...,
      ...,
    }

To output the changelog in string format, use the ``pprint=True`` keyword argument, e.g. 
``compute_changelog('dr17', 'dr16', pprint=True)``, which pretty-prints the changelog
into a nicer format.  See :ref:`Tree Evolution <tree_evolve>` for an example pretty-printing 
of the changelog between DR17 and DR16. 
