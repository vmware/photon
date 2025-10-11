UMASK := 0022
SHELL := /bin/bash
CONF := build-config.json

.PHONY: all

RELEASE_BRANCH_ID = $(shell pwd | sed 's|/|-|g')
FIRST_PASS_MARKER = /tmp/.first-pass$(RELEASE_BRANCH_ID)
$(shell rm -f $(FIRST_PASS_MARKER))

export FIRST_PASS_MARKER

all:
	@if [ -n "$(pkgs)" ]; then \
		umask $(UMASK) && python3 build.py -c $(CONF) --pkgs "$(pkgs)"; \
	elif [ "$(BUILD_EXTRA_PKGS)" = "1" ]; then \
		umask $(UMASK) && python3 build.py -c $(CONF) -t extra-packages; \
	else \
		umask $(UMASK) && python3 build.py -c $(CONF) -t packages; \
	fi

%:
	umask $(UMASK) && python3 build.py -c $(CONF) -t "$@" && \
	if [[ "$@" != clean* ]]; then \
		touch $(FIRST_PASS_MARKER); \
	fi
