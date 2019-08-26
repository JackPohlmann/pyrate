# Need to find a balance for installation.
# Can setup.py be used in a similar manner to Makefile?
#
# NOTE: Makefile can be used inside the container, but setup.py should be used
# 	for the primary installation since it is OS-agnostic.

NAME = pyrate
VERSION = $(shell grep -m 1 'VERSION' pyrate.py | awk '{ print $3 }')

DESTDIR ?= /
PREFIX ?= /usr/local


default: test install

docker_install:
	@echo "Install the docker container."

docker_uninstall:
	@echo "Uninstall the docker container."

local_install:
	@echo "Install the local files."

local_uninstall:
	@echo "Uninstall the local files."

install: local_install docker_install
	
uninstall: local_uninstall docker_uninstall

test:
	@echo "Run Python unit tests."

.PHONY: default docker_install docker_unintstall \
	local_install local_uninstall \
        install uninstall test	
