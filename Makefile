ifndef CONF
	CONF := build-config.json
endif

COMMON_BRANCH_PATH ?= $(shell jq -r '.["common-branch-path"]' "$(CONF)")
STAGE_PATH ?= $(shell jq -r '.["stage-path"]' "$(CONF)")

export RELEASE_BRANCH_PATH := $(PWD)
export STAGE_PATH := $(shell realpath $(STAGE_PATH))


%:
	@if [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew 'enable|yes|True')" ]; then\
		(pushd $(COMMON_BRANCH_PATH) && python3 build.py -c $(CONF) -t extra-packages);\
		popd; \
	else\
		(pushd $(COMMON_BRANCH_PATH) && python3 build.py -c $(CONF) -t $@);\
		popd; \
	fi