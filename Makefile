CONF := build-config.json

.PHONY: all

all:
	@if [ -n "$(pkgs)" ]; then \
		python3 build.py -c $(CONF) --pkgs "$(pkgs)"; \
	elif [ "$(BUILD_EXTRA_PKGS)" = "1" ]; then \
		python3 build.py -c $(CONF) -t extra-packages; \
	else \
		python3 build.py -c $(CONF) -t packages; \
	fi

%:
	@python3 build.py -c $(CONF) -t $@
