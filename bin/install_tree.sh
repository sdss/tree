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
# Install Module files
#
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
        print_and_run cp -pf  ${module} ${treemodules}/tree/${version}
    done
    print_and_run cp -pf .version ${treemodules}/tree
else
    echo "Unable to write to ${treemodules}, skipping."
fi
