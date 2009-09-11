#
# Makefile for SAS ups table.
#
# This Makefile is used to properly set the $SAS_ROOT environment variable
# in the sas.table.
#
# If the script sas_root.sh recognizes the value of the $HOSTNAME variable, that will be
# used.  Otherwise, a user can pre-set the value of $SAS_ROOT in the
# environment & that will be used.  If neither case is satisfied, the user
# will be prompted to enter a value for $SAS_ROOT.
#
# $Id$
#
SHELL = /bin/sh

all:
	/bin/bash ./sas_root.sh

clean:
	- /bin/rm -f *~ sas.table
	- /bin/mv sas.table.orig sas.table

