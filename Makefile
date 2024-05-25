ifndef CONF
	CONF := build-config.json
endif

%:
	@if [ -n "$(shell echo $(BUILD_EXTRA_PKGS) | grep -Ew "enable|yes|True")" ]; then\
		python3 build.py -c $(CONF) -t extra-packages;\
	else\
		python3 build.py -c $(CONF) -t $@;\
	fi

help:
	@python3 build.py --help
