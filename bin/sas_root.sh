#!/bin/bash
#
# $Id$
#
# If $SAS_ROOT is already set, use it.
#
if test -z "${SAS_ROOT}"; then
    SAS_ROOT=undefined
    if test ${HOSTNAME%.lbl.gov} != ${HOSTNAME}; then
        SAS_ROOT=/clusterfs/riemann/raid006
    elif test ${HOSTNAME%.lbnl.us} != ${HOSTNAME}; then
        SAS_ROOT=/clusterfs/riemann/raid006
    elif test ${HOSTNAME%.nyu.edu} != ${HOSTNAME}; then
        SAS_ROOT=/mount/coma1/bw55/sdss3/mirror
    elif test ${HOSTNAME%.nersc.gov} != ${HOSTNAME}; then
        SAS_ROOT=/project/projectdirs/boss
    else
        echo
        echo "Could not set \$SAS_ROOT based on hostname or environment variable."
        echo "\$SAS_ROOT needs to be set to define the root of the SAS tree."
        echo "You will now be given the opportunity to enter a directory name."
        echo "It would be nice if that directory actually existed, but that"
        echo "is not strictly necessary to make this installation work."
        echo
        echo "Please use a directory name that is an absolute path, for example:"
        echo "/my/sas/root"
        echo
        echo "For future reference, you can set the environment variable"
        echo "\$SAS_ROOT in advance to avoid this step."
        echo
        read -t 60 -p "Enter a directory to serve as \$SAS_ROOT: " userdir
        if test $? = 0; then
            SAS_ROOT=${userdir}
        else
            echo "Error: SAS_ROOT directory not set!" >&2
            exit 1
        fi
    fi
    echo ${SAS_ROOT}/foo
else
    echo ${SAS_ROOT}
fi
