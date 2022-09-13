ifndef CONF
	CONF := build-config.json
endif

%:
	@./build.py -c $(CONF) -t $@
