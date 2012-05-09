#!/bin/sh
#
# Install files in the etc directory.
#
# $Id$
#
# Check for INSTALL_DIR
#
if [ -z "${INSTALL_DIR}" ]; then
    echo "INSTALL_DIR is not defined, skipping this step."
    exit 0
fi
#
# Install EUPS files
#
installbase=$(dirname ${INSTALL_DIR})
for table in *.table; do
    version=$(echo ${table} | cut -d. -f1)
    echo mkdir -p ${installbase}/${version}/ups
    echo cp -pf ${table} ${installbase}/${version}/ups/tree.table
    #
    # If EUPS_PATH is set, assume that the eups command is available
    #
    if [ -n "${EUPS_PATH}" ]; then
        if [ $(basename $(dirname ${installbase})) = 'NULL' ]; then
            flavor='-f NULL'
        else
            flavor=''
        fi
        grep -qi 'current = true' ../data/${version}.cfg
        if [ $? = 0 ]; then
            current='-c'
        else
            current=''
        fi
        echo eups declare ${current} ${flavor} -r ${installbase}/${version} tree ${version}
    fi
done
#
# Install Module files
#
installbase=$(dirname ${installbase})
treemodules=''
for m in $(echo ${MODULEPATH} | tr ':' ' '); do
    if [ -d ${m}/tree ]; then
        treemodules=${m}
    fi
done
if [ -z "${treemodules}" ]; then
    treemodules=$(echo ${MODULEPATH} | cut -d: -f1)
    echo mkdir -p ${treemodules}/tree
fi
for module in *.module; do
    version=$(echo ${module} | cut -d. -f1)
    # echo cp -pf ${module} ${treemodules}/tree/${version}
    echo "cat ${module} | sed \"s%@INSTALL_DIR@%${installbase}%\" > ${treemodules}/tree/${version}"
done
echo cp -pf .version ${treemodules}/tree

