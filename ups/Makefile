###############################################################################
# Sloan Digital Sky Survey III (SDSS-III)
# Code for product: tree
#
# This Makefile & all Makefiles in this product are GNU make compliant.
# Please help keep them that way.  See
# http://www.gnu.org/software/make/manual/make.html
#
# $Id$
#
###############################################################################
#
# Makefile for tree ups table.
#
# This Makefile is used to properly set the $SAS_ROOT environment variable
# in the tree.table.
#
# If the script sas_root.sh recognizes the value of the $HOSTNAME variable,
# that will be used.  Otherwise, a user can pre-set the value of $SAS_ROOT in
# the environment & that will be used.  If neither case is satisfied, the user
# will be prompted to enter a value for $SAS_ROOT.
#
# $Id$
#
#
# This line helps prevent make from getting confused in the case where you
# have a file named 'clean'.
#
.PHONY : clean
#
# This generates the final tree.table file.
#
all:
	/bin/bash ./sas_root.sh
#
# GNU make pre-defines $(RM).  The - in front of $(RM) causes make to
# ignore any errors produced by $(RM).
#
clean:
	- $(RM) *~ tree.table
	- /bin/mv tree.table.orig tree.table

