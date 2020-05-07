
.. _addpaths:

Adding Paths into the Tree
==========================

The SDSS `tree` product is designed to simplify the environment setup and directory system for navigating SDSS
data products.  `sdss_access <http://sdss-access.readthedocs.io/en/stable>`_ is a product designed to facilitate
easy local and remote file access, as well as easy downloading of remote files.  With help from the `tree`,
it dynamically constructs filesystem paths, eliminating the need know the exact location and nomenclature of
SDSS files on disk. Paths to all SDSS files are defined in the ``[PATHS]`` ini section of the `tree`'s environment
configuration files, e.g. `sdsswork.cfg <https://github.com/sdss/tree/blob/master/data/sdsswork.cfg>`_ or
`dr16.cfg <https://github.com/sdss/tree/blob/master/data/dr16.cfg>`_. Paths must be defined here in order
to be used by the `sdss_access` product.

To add a new template path definition into the SDSS tree product, please follow the steps below.

Fork and Clone the Github repo
------------------------------

You must have an account on Github.  If you do not already have one, you can sign up
`here <https://github.com/join>`_. Once you have a Github account set up, fork the ``tree`` repo.  Follow
the instructions in `Forking a Repo <https://help.github.com/en/articles/fork-a-repo>`_ for help forking a
repo and `keeping it in sync <https://help.github.com/en/articles/syncing-a-fork>`_ with the original source.

Define a New Path template
--------------------------

Before you begin make sure your data product has a proper location on the SDSS Science Archive
Server (SAS) and has an appropriate environment variable set in the tree configuration files,
defining its base location.  If you are unsure if this has been done already, or how to do this, please contact
the SDSS Data Team (helpdesk@sdss.org).

New paths are defined in the ``[PATHS]`` ini sections of the ``tree`` environment configuration files.  See the
`DR16 environment config file <https://github.com/sdss/tree/blob/master/data/dr16.cfg>`_ as an example.  To learn where
you should define your path, go :ref:`here <path-where>`.  Each ``[PATHS]`` ini section contains a series of
"path templates", which are abstractions to data products using the Jinja2 templating system.
The syntax format of a new path entry is the following:
::

    short_name = template_file_path

The **short_name** is a shorthand string representation of your file. The **template_file_path** is the full
path location to your file, constructed in a template format using environment variables, and {}
template keyword names.

For example, consider a DR15 MaNGA cube,
https://dr15.sdss.org/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGCUBE.fits.gz. Since there
are many MaNGA cubes across multiple releases of data, we replace specific names, versions,
parameters, etc, with a template keyword indicated with {} notation. The path definition for a cube is as follows:
::

    mangacube = $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}CUBE.fits.gz

We've given the cube a short_name of **mangacube**. The template_file_path begins with the MANGA_SPECTRO_REDUX
environment variable, which makes the file agnostic to its base location.  The template_file_path also has replaced
the specific markers:

* v2_4_3 with {drpver} - the Data Reduction Pipeline(DRP) version
* 8485 with {plate} - the plate ID
* 1901 with {ifu} - the IFU bundle name
* LOG with {wave} - the wavelength sampling used in the cube, e.g. LOG or LIN

Now we can easily define paths to new files, e.g. files from different releases, or different parameters easily
without knowing the exact full path location.

Naming Conventions and Guidelines
---------------------------------

When defining a new path template, please adhere to the following guidelines:

* Each short_name must be unique.  Do not use a name that may map to a different file.
* Every template_file_path must start with an environment variable, defined in the tree configs.
* Use easily understood keyword parameter names, consisting only of alphabetic characters.
* Try to be as consistent as possible with other path entry naming conventions, e.g. if most entries use "plate", use "plate" rather than "plateid".
* Use minimal string formatting in keyword names, e.g. zero-padding for integer variables ``{run:0>6}``

Build and Test your Path
------------------------

You can test your new path defintion using `sdss_access.path.Path`.  `Path` takes as input the **short_name**, and
the series of keyword arguments specifying the variables needed to define the full path.  The keyword argument names
are the same names defined in the **template_file_path**.
::

    >>> from sdss_access.path import Path
    >>> path = Path()

    >>> # build a new local path using Path.full
    >>> filepath = path.full('mangacube', drpver='v2_4_3', plate=8485, ifu=1901, wave='LOG')
    >>> print(filepath)
        '/Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGCUBE.fits.gz'

    >>> # try a new path
    >>> path.full('mangacube', drpver='v2_3_3', plate=7443, ifu=12701, wave='LIN')
        '/Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v2_3_1/7443/stack/manga-7443-12701-LINCUBE.fits.gz'

To test a path to a public file from a DR, e.g. DR15, simply specify the proper release.  The ``public`` keyword will
automatically get set to ``True``.  However you can always ensure it by setting it explicitly.
::

    >>> path = Path(public=True, release='DR15')
    >>> path.full('mangacube', drpver='v2_4_3', plate=8485, ifu=1901, wave='LOG')
        '/Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGCUBE.fits.gz'

.. _path-where:

Where Do I Put My New Definitions?
----------------------------------

Paths must minimally be defined inside the ``sdsswork.cfg``, which represents the everyday working SDSS environment.
When data products are released during public data releases (DRs), those paths must also be defined in one of
the ``drXX.cfg`` environment files. For example, suppose you have been working with two new data files, a FITS
file and a csv file, but are only planning on releasing the FITS file for SDSS DR15.  The path definition for the
csv file would be placed inside the ``[PATHS]`` ini section in ``sdsswork.cfg``, while the FITS file path definition would
go inside both the ``sdsswork.cfg`` and ``dr15.cfg`` files.

The ``sdsswork.cfg`` environment configuration should always contain the most up-to-date definition of a path.  Tracking
changes in path locations occurs in public ``drXX.cfg`` files only.

What If I Change My Product Path or Filename Between Releases?
--------------------------------------------------------------

Suppose you released a FITS file in DR15, found at ``$MY_VAC/path/v1/data_product.fits``.  Its path definition in
the ``dr15.cfg`` was defined as
::

    [PATHS]
    myfits = $MY_VAC/path/{version}/data_product.fits

However, now for DR16, you have moved the location of the FITS file into a new sub-directory and renamed it to encode
additional information, such that its new location is ``$MY_VAC/path/v2/subdir/data_product_A.fits``.  Within the
``dr16.cfg`` define the path in its new state
::

    [PATHS]
    myfits = $MY_VAC/path/{version}/subdir/data_product_{name}.fits

The path to your file has been properly versioned between DR15 and DR16.  Remember to update the working environment,
``sdsswork.cfg`` with your new path definition.  You can check for the correct paths with `sdss_access.path.Path`:
::

    >>> from sdss_access.path import Path

    >>> # loading paths for DR15
    >>> path = Path(release='DR15')
    >>> path.full('myfits', version='v1')
    '/files/dr15/vacs/path/v1/data_product.fits'

    >>> # loading paths for DR16
    >>> path = Path(release='DR15')
    >>> path.full('myfits', version='v2', name='A')
    '/files/dr16/vacs/path/v2/subdir/data_product_A.fits'

    >>> # loading paths from sdsswork
    >>> path = Path()
    >>> path.full('myfits', version='v2', name='A')
    '/files/sdsswork/vacs/path/v2/subdir/data_product_A.fits'

.. _path-svn:

Defining Paths to Data Files in SVN
-----------------------------------

If you want to define a path to a data file that is a part of a SVN software product, e.g. `plPlugMapP` plugging file, or a MaNGA preimaging file,
you must define two things: an environment variable and a path template.  The environment variable must have the following syntax
::

    [PRODUCT_NAME]_DIR = $PRODUCT_ROOT/path/to/top_level/directory

and the path template is defined as usual
::

    short_name = $[PRODUCT_NAME]_DIR/template_path_definition

The defined environment variable must start with the **$PRODUCT_ROOT** environment variable.  The **$PRODUCT_ROOT** is a special environment
variable that represents the top level directory where your svn products are installed.  You do not have to define this.  It automatically gets
defined when the ``tree`` python package is imported and instantiated.  It attempts to identify the root software installation directory and
sets itself to the first defined path it finds.  It looks for the following defined environment variables in order of precedence:

- PRODUCT_ROOT
- SDSS_SVN_ROOT
- SDSS_INSTALL_PRODUCT_ROOT
- SDSS_PRODUCT_ROOT
- SDSS4_PRODUCT_ROOT

You can also manually set the product root in Python with ``tree.set_product_root()`` method.  Or you can optionally set the `PRODUCT_ROOT`
manually by setting the `PRODUCT_ROOT` parameter in your custom config file, ``~/.config/tree/tree.yml``

As an example, let's take the addition of the MaNGA preimaging files, which are a part of the ``mangapreim`` svn software repository.
Within the `sdsswork.cfg <https://github.com/sdss/tree/blob/master/data/sdsswork.cfg>`_ config file, we define the environment variable
that points to the main ``trunk`` of the product in the `[MANGA]` environment section, and a new path to the pre-imaging file in the `[PATHS]`
section.
::

    [MANGA]
    MANGAPREIM_DIR = $PRODUCT_ROOT/data/manga/mangapreim/trunk

    [PATHS]
    mangapreimg = $MANGAPREIM_DIR/data/{designgrp}/{designid}/preimage-{mangaid}_irg.jpg

If the product was also released as a tag for a public data release, and hosted on ``svn.sdss.org/public``, then you can set
the environment variable to the proper location in the appropriate ``drXX.cfg`` file.  In our MaNGA pre-imaging example, we set the following
within the `dr15.cfg <https://github.com/sdss/tree/blob/master/data/dr15.cfg>`_ file.
::
    [MANGA]
    MANGAPREIM_DIR = $PRODUCT_ROOT/data/manga/mangapreim/tags/v2_5

    [PATHS]
    mangapreimg = $MANGAPREIM_DIR/data/{designgrp}/{designid}/preimage-{mangaid}_irg.jpg

The path is now available in ``sdss_access``, with the proper versioning in place.
::

    from sdss_access.path import Path

    # load the paths for sdsswork
    path = Path()
    path.full('mangapreimg', designid=8405, designgrp='D0084XX', mangaid='1-42007')
    '/Users/Brian/Work/sdss/data/manga/mangapreim/trunk/data/D0084XX/8405/preimage-1-42007_irg.jpg'

    # load the paths for DR15
    path = Path(release='DR15')
    path.full('mangapreimg', designid=8405, designgrp='D0084XX', mangaid='1-42007')
    '/Users/Brian/Work/sdss/data/manga/mangapreim/v2_5/data/D0084XX/8405/preimage-1-42007_irg.jpg'

    path.url('mangapreimg', designid=8405, designgrp='D0084XX', mangaid='1-42007')
    'https://svn.sdss.org/public/data/manga/mangapreim/tags/v2_5/data/D0084XX/8405/preimage-1-42007_irg.jpg'

For additional information on how to handle SVN paths with ``sdss_access``, for example, how to deal with locally checked out products
managed with ``Modules`` environment manager, see `Accessing SVN Paths <https://sdss-access.rtfd.io/en/latest/intro.html#accessing-paths-to-data-files-in-svn>`_.

Advanced Items of Note
----------------------

**Keyword Variable Formatting**:
    You can format the keyword parameter names using
    `Python's String Format Spec <https://docs.python.org/3/library/string.html#formatspec>`_, e.g. if you need
    to zero-pad integer variables, or constrain number of digits.  See `{run:0>6}` as an example.

**Special Functions**:
    Some parts of the template_file_path use a "path substitution" syntax, designated as ``@function_name``.  These
    names resolve to functions that are called by `sdss_access` during path reconstruction to perform more
    complex substitution.  See `@platedir` in the ``plateHoles`` entry as an example.


Submit a Pull Request
---------------------

Once you are done, submit a Pull Request.  Someone will review your changes.  Once approved, your Pull Request will
be merged into the ``master`` branch.  Your path will then become available during the next tag and software release.


