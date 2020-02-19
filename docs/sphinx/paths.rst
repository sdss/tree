
.. _addpaths:

Adding Paths into the Tree
==========================

The SDSS `tree` product is designed to simplify the environment setup and directory system for navigating SDSS 
data products.  `sdss_access <http://sdss-access.readthedocs.io/en/stable>`_ is a product designed to facilitate 
easy local and remote file access, as well as easy downloading of remote files.  With help from the `tree`, 
it dynamically constructs filesystem paths, eliminating the need know the exact location and nomenclature of 
SDSS files on disk. Paths to all SDSS files are defined in the `tree`'s 
`sdss_paths.ini <https://github.com/sdss/tree/blob/master/data/sdss_paths.ini>`_ file. Paths must be defined 
here in order to be used by the `sdss_access` product.   

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

New paths are defined in the ``data/sdss_paths.ini`` file.  This file contains a series of "path templates", 
which are abstractions to data products using the Jinja2 templating system.  The syntax format of a new path 
entry is the following:
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

Remember, to test a path to a public file from a DR, e.g. DR15, you need to specify the release and a `public=True`
boolean when instantiating the `Path` object.
::

    >>> path = Path(public=True, release='DR15')
    >>> path.full('mangacube', drpver='v2_4_3', plate=8485, ifu=1901, wave='LOG')
        '/Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGCUBE.fits.gz'

Advanced Items of Note
----------------------

**Keyword Variable Formatting**:
    You can format the keyword parameter names using 
    `Python's String Format Spec <https://docs.python.org/3/library/string.html#formatspec>`_, e.g. if you need 
    to zero-pad integer variables, or constrain number of digits.  See `{run:0>6}` as an example.   

**Special Functions**:
    Some parts of the template_file_path use a "path substitution" syntax, designated as ``%function_name``.  These
    names resolve to functions that are called by `sdss_access` during path reconstruction to perform more 
    complex substitution.  See `%platedir` in the ``plateHoles`` entry as an example.


Submit a Pull Request
---------------------

Once you are done, submit a Pull Request.  Someone will review your changes.  Once approved, your Pull Request will
be merged into the ``master`` branch.  Your path will then become available during the next tag and software release.  


