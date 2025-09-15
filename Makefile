SHELL := /bin/bash

CONF := build-config.json

.PHONY: all

.DEFAULT_GOAL := all

TOOLS := jq
$(foreach tool, $(TOOLS), \
	$(if $(shell command -v $(tool)), , $(error "$(tool) is not installed. Please install $(tool) to proceed.")) \
)

COMMON_BRANCH_PATH := $(shell jq -r '.["common-branch-path"]' "$(CONF)")
RELEASE_BRANCH_PATH := $(shell pwd)
STAGE_PATH := $(shell realpath $(shell jq -r '.["stage-path"]' "$(CONF)"))

RELEASE_BRANCH_ID = $(shell pwd | sed 's|/|-|g')
FIRST_PASS_MARKER = /tmp/.first-pass$(RELEASE_BRANCH_ID)
$(shell rm -f $(FIRST_PASS_MARKER))

export COMMON_BRANCH_PATH RELEASE_BRANCH_PATH STAGE_PATH FIRST_PASS_MARKER

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
	fi \
	)

%:
	@$(call with_pushd, \
	python3 build.py -c $(CONF) -t "$@" && \
	if [[ "$@" != clean* ]]; then \
		touch $(FIRST_PASS_MARKER); \
	fi \
	)
