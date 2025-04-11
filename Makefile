CONF := build-config.json

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
	@if [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew "enable|yes|True")" ]; then\
		python3 build.py -c $(CONF) -t extra-packages;\
	else\
		python3 build.py -c $(CONF) -t $@;\
	fi

help:
	@python3 build.py --help
