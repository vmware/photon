ifndef CONF
	CONF := build-config.json
endif

%:
	@python3 build.py -c $(CONF) -t $@
