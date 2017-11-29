# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-11-29 02:11:44
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-11-29 02:13:11

from __future__ import print_function, division, absolute_import
from invoke import Collection, task


@task
def clean(ctx):
    ''' Cleans up the crap before a Pip build '''
    print('Cleaning')
    ctx.run("rm -rf htmlcov")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")


@task(clean)
def deploy(ctx):
    ''' Deploy the project to pypi '''
    print('Deploying to Pypi!')
    ctx.run("python setup.py sdist bdist_wheel --universal")
    ctx.run("twine upload dist/*")


# create a collection of tasks
ns = Collection(clean, deploy)

