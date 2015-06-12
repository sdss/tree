#!/bin/bash
#
# $Id$
#
# If $SAS_BASE_DIR is already set, use it.
#
if test -z "${SAS_BASE_DIR}"; then
    SAS_BASE_DIR=undefined
    if test ${HOSTNAME%.lbl.gov} != ${HOSTNAME}; then
        SAS_BASE_DIR=/clusterfs/riemann/raid006
    elif test ${HOSTNAME%.lbnl.us} != ${HOSTNAME}; then
        SAS_BASE_DIR=/clusterfs/riemann/raid006
    elif test ${HOSTNAME%.nyu.edu} != ${HOSTNAME}; then
        SAS_BASE_DIR=/mount/coma1/bw55/sdss3/mirror
    elif test ${HOSTNAME%.nersc.gov} != ${HOSTNAME}; then
        SAS_BASE_DIR=/global/projecta/projectdirs/sdss/data/sdss
    else
        echo
        echo "Could not set \$SAS_BASE_DIR based on hostname or environment variable."
        echo "\$SAS_BASE_DIR needs to be set to define the root of the SAS tree."
        echo "You will now be given the opportunity to enter a directory name."
        echo "It would be nice if that directory actually existed, but that"
        echo "is not strictly necessary to make this installation work."
        echo
        echo "Please use a directory name that is an absolute path, for example:"
        echo "/my/sas/root"
        echo
        echo "For future reference, you can set the environment variable"
        echo "\$SAS_BASE_DIR in advance to avoid this step."
        echo
        read -t 60 -p "Enter a directory to serve as \$SAS_BASE_DIR: " userdir
        if test $? = 0; then
            SAS_BASE_DIR=${userdir}
        else
            echo "Error: SAS_BASE_DIR directory not set!" >&2
            exit 1
        fi
    fi
fi
echo ${SAS_BASE_DIR}
