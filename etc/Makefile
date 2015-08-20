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
# Make sure SAS_BASE_DIR is set
#
export SAS_BASE_DIR = $(shell ../bin/sas_base.sh)
#
# This should compile all code prior to it being installed
#
all :
	../bin/setup_tree.py -t $(dir $(CURDIR))
	../bin/install_tree.sh
#
#
#
env_links :
	../bin/env_links.py
#
# GNU make pre-defines $(RM).  The - in front of $(RM) causes make to
# ignore any errors produced by $(RM).
#
clean :
	- $(RM) *~ *.sh *.csh *.module *_version .version
