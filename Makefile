###############################################################################
# Sloan Digital Sky Survey (SDSS)
# Code for product: tree
###############################################################################

SHELL = /bin/sh
#
.c.o :
	$(CC) -c $(CCCHK) $(CFLAGS) $*.c
#
CFLAGS  = 

SUBDIRS = ups 
INSTALL_DIR = $(TREE_DIR)

all :
	@ for f in $(SUBDIRS); do \
		(cd $$f ; echo In $$f; $(MAKE) $(MFLAGS) all ); \
	done

# Install things in their proper places in $(INSTALL_DIR)
install :
	@echo "You should be sure to have updated before doing this."
	@echo ""
	@if [ "$(INSTALL_DIR)" = "" ]; then \
		echo You have not specified a destination directory >&2; \
		exit 1; \
	fi 
	@if [ -e $(INSTALL_DIR) ]; then \
		echo The destination directory already exists >&2; \
		exit 1; \
	fi 
	@echo ""
	@echo "You will be installing in \$$INSTALL_DIR=$(INSTALL_DIR)"
	@echo "I'll give you 5 seconds to think about it"
	@sleep 5
	@echo ""
	@ rm -rf $(INSTALL_DIR)
	@ mkdir $(INSTALL_DIR)
	@ cp -rpf * $(INSTALL_DIR)

clean :
	- /bin/rm -f *~ core
	@ for f in $(SUBDIRS); do \
		(cd $$f ; echo In $$f; $(MAKE) $(MFLAGS) clean ); \
	done
