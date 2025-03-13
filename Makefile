SHELL := /bin/bash

CONF := build-config.json

COMMON_BRANCH_PATH ?= $(shell jq -r '.["common-branch-path"]' "$(CONF)")
STAGE_PATH ?= $(shell jq -r '.["stage-path"]' "$(CONF)")

export RELEASE_BRANCH_PATH := $(shell pwd)
export STAGE_PATH := $(shell realpath $(STAGE_PATH))

.PHONY: all

all:
	@if [ -n "$(pkgs)" ]; then \
		(pushd $(COMMON_BRANCH_PATH) > /dev/null && \
		python3 build.py -c $(CONF) --pkgs "$(pkgs)" && \
		popd > /dev/null); \
	elif [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew "enable|yes|True|1")" ]; then \
		(pushd $(COMMON_BRANCH_PATH) > /dev/null && \
		python3 build.py -c $(CONF) -t extra-packages && \
		popd > /dev/null); \
	else \
		(pushd $(COMMON_BRANCH_PATH) > /dev/null && \
		python3 build.py -c $(CONF) -t packages && \
		popd > /dev/null); \
	fi

%:
	@if [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew 'enable|yes|True')" ]; then\
		(pushd $(COMMON_BRANCH_PATH) > /dev/null && \
		python3 build.py -c $(CONF) -t extra-packages && \
		popd > /dev/null); \
	else\
		(pushd $(COMMON_BRANCH_PATH) > /dev/null && \
		 python3 build.py -c $(CONF) -t $@ && \
		popd > /dev/null); \
	fi
