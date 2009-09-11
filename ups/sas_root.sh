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
    export SAS_ROOT
fi
echo
echo "\$SAS_ROOT = ${SAS_ROOT}"
echo
cp tree.table tree.table.orig
cat >> tree.table <<EOT
#
# Base of the whole SAS tree
#
envSet(SAS_ROOT,${SAS_ROOT})
#
# Raw data from APO
#
envSet(STAGING_DATA,\${SAS_ROOT}/apo_staging)
#
# Shared directories
#
envSet(COMMON_ROOT,\${SAS_ROOT}/common)
#
# CAS loading area
#
envSet(CAS_LOAD,\${SAS_ROOT}/casload)
#
# BOSS directories
#
envSet(BOSS_ROOT,\${SAS_ROOT}/groups/boss)
envSet(PHOTO_DATA,\${BOSS_ROOT}/photo/data)
envSet(PHOTO_REDUX,\${BOSS_ROOT}/photo/redux)
envSet(PHOTO_SKY,\${BOSS_ROOT}/photo/sky)
envSet(BOSS_SPECTRO_DATA,\${BOSS_ROOT}/spectro/data)
envSet(BOSS_SPECTRO_REDUX,\${BOSS_ROOT}/spectro/redux)
envSet(ASTROLOG_DIR,\${BOSS_ROOT}/spectro/astrolog)
envSet(BOSS_TARGET,\${BOSS_ROOT}/target)
envSet(PHOTO_SWEEP_BASE,\${BOSS_ROOT}/sweeps)
envSet(PHOTO_RESOLVE_BASE,\${BOSS_ROOT}/resolve)
envSet(PHOTO_CALIB_BASE,\${BOSS_ROOT}/calib)
envSet(PHOTO_SWEEP,\${PHOTO_SWEEP_BASE}/2009-06-14)
envSet(PHOTO_RESOLVE,\${PHOTO_RESOLVE_BASE}/2009-06-14)
envSet(PHOTO_CALIB,\${PHOTO_CALIB_BASE}/2009-06-14/calibs/default0)
envSet(BOSS_LSS_REDUX,\${BOSS_ROOT}/lss)
envSet(BOSS_MATCH,\${BOSS_ROOT}/match)
envSet(BOSS_PHOTOOBJ,\${BOSS_ROOT}/photoObj)
#
# MARVELS directories
#
envSet(MARVELS_ROOT,\${SAS_ROOT}/groups/marvels)
envSet(MARVELS_DATA,\${MARVELS_ROOT}/spectro/data)
envSet(MARVELS_REDUX,\${MARVELS_ROOT}/spectro/redux)
envSet(MARVELS_TARGET,\${MARVELS_ROOT}/target)
#
# APOGEE directories
#
envSet(APOGEE_ROOT,\${SAS_ROOT}/groups/apogee)
envSet(APOGEE_DATA,\${APOGEE_ROOT}/spectro/data)
envSet(APOGEE_REDUX,\${APOGEE_ROOT}/spectro/redux)
envSet(APOGEE_TARGET,\${APOGEE_ROOT}/target)
#
# SEGUE-II directories
#
envSet(SEGUE2_ROOT,\${SAS_ROOT}/groups/segue2)
envSet(SPECTRO_REDUX,\${COMMON_ROOT}/sdss-spectro/redux)
envSet(RAWDATA_DIR,\${COMMON_ROOT}/sdss-spectro/raw)
envSet(SSPP_REDUX,\${SEGUE2_ROOT}/sspp)
envSet(SEGUE2_TARGET,\${SEGUE2_ROOT}/target)
#
# SDSS-I, -II Archival data
#
envSet(ARCHIVE_ROOT,\${SAS_ROOT}/archive)
envSet(SDSS_TILING,\${ARCHIVE_ROOT}/sdss-tiling)
envSet(SEGUE_TARGET,\${ARCHIVE_ROOT}/segue1/target)
envSet(SDSS_PLATE,\${ARCHIVE_ROOT}/plates)
#
# Plate design directories
#
envSet(PLATE_DESIGN_DATA,\${SAS_ROOT}/plates)
EOT
