ifndef CONF
	CONF := config.json
endif

%:
	@./build.py -c $(CONF) -t $@
