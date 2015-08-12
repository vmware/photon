import os
import subprocess
import commons

install_phase = commons.PRE_INSTALL
enabled = True

def execute(name, ks_config, config, root):

	if ks_config:
		config['disk'] = commons.partition_disk(ks_config['disk'])
