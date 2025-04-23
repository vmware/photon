SHELL := /bin/bash

CONF := build-config.json

COMMON_BRANCH_PATH ?= $(shell jq -r '.["common-branch-path"]' "$(CONF)")
STAGE_PATH ?= $(shell jq -r '.["stage-path"]' "$(CONF)")

export RELEASE_BRANCH_PATH := $(shell pwd)
export STAGE_PATH := $(shell realpath $(STAGE_PATH))

.PHONY: all

define with_pushd
	pushd $(COMMON_BRANCH_PATH) > /dev/null && \
	{ $(1); } && \
	popd > /dev/null
endef

all:
	@$(call with_pushd, \
	if [ -n "$(pkgs)" ]; then \
		python3 build.py -c $(CONF) --pkgs "$(pkgs)"; \
	elif [ "$(BUILD_EXTRA_PKGS)" = "1" ]; then \
		python3 build.py -c $(CONF) -t extra-packages; \
	else \
		python3 build.py -c $(CONF) -t packages; \
	fi; \
	)

%:
	@$(call with_pushd, python3 build.py -c $(CONF) -t $@)
