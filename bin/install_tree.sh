#!/bin/sh
#
# Install files in the etc directory.
#
# $Id: install_tree.sh $
#
# Define function
#
function print_and_run {
    echo "$@"
    eval "$@"
}
#
# Check for INSTALL_DIR
#
if [ -z "${TREE_DIR}" ]; then
    echo "TREE_DIR is not defined, skipping install."
    exit 0
fi
#
# Install version files
#
treebase=$(dirname ${TREE_DIR})
for table in *.table; do
    version=$(echo ${table} | cut -d. -f1)
    print_and_run mkdir -p ${treebase}/${version}/bin
    print_and_run cp -pf ${version}_version ${treebase}/${version}/bin/tree_version
    print_and_run chmod +x ${treebase}/${version}/bin/tree_version
done
#
# Install Module files
#
treebase=$(dirname ${treebase})
treemodules=''
for m in $(echo ${MODULEPATH} | tr ':' ' '); do
    if [ -d ${m}/tree ]; then
        treemodules=${m}
        break
    fi
done
if [ -z "${treemodules}" ]; then
    treemodules=$(echo ${MODULEPATH} | cut -d: -f1)
fi
if [ -w "${treemodules}" ]; then
    print_and_run mkdir -p ${treemodules}/tree
    for module in *.module; do
        version=$(echo ${module} | cut -d. -f1)
        print_and_run "cat ${module} | sed \"s%@INSTALL_DIR@%${treebase}%\" > ${treemodules}/tree/${version}"
    done
    print_and_run cp -pf .version ${treemodules}/tree
else
    echo "Unable to write to ${treemodules}, skipping."
fi
