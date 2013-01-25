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
# This line helps prevent make from getting confused in the case where you
# have a file named 'clean'.
#
.PHONY : clean
#
# Make sure SAS_ROOT is set
#
SAS_ROOT = $(shell ../bin/sas_root.sh)
#
# This should compile all code prior to it being installed
#
all :
	../bin/setup_tree.py --root=$(SAS_ROOT)
#
#
#
install :
	../bin/install.sh
	../bin/env_links.py --root=$(SAS_ROOT)
#
# GNU make pre-defines $(RM).  The - in front of $(RM) causes make to
# ignore any errors produced by $(RM).
#
clean :
	- $(RM) *~ *.sh *.csh *.table *.module *_version .version
