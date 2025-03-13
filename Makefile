CONF := build-config.json
ARG_COUNT := $(words $(MAKECMDGOALS))

ifneq ($(ARG_COUNT),1)
PKGS := "$(shell echo $(MAKECMDGOALS) | tr ' ' ',')"
LAST_TARGET := $(lastword $(MAKECMDGOALS))
endif

.PHONY: all

all:
	@if [ -n "$(pkgs)" ]; then \
		python3 build.py -c $(CONF) --pkgs "$(pkgs)"; \
	elif [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew "enable|yes|True|1")" ]; then \
		python3 build.py -c $(CONF) -t extra-packages; \
	else \
		python3 build.py -c $(CONF) -t packages; \
	fi

%:
	@if [ $(ARG_COUNT) -eq 1 ]; then \
		python3 build.py -c $(CONF) -t $@; \
	elif [ "$@" = "$(LAST_TARGET)" ]; then \
		python3 build.py -c $(CONF) --pkgs "$(PKGS)"; \
	fi
