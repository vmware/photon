import os
import subprocess
import commons

install_phase = commons.PRE_INSTALL
enabled = True

def execute(name, ks_config, config, root):

	if ks_config:
		docker_partition_size = None
		swap_partition_size = None
		if 'docker_partition_size' in ks_config:
			docker_partition_size = ks_config['docker_partition_size']
		if 'swap_partition_size' in ks_config:
			swap_partition_size = ks_config['swap_partition_size']
		config['disk'] = commons.partition_disk(ks_config['disk'], docker_partition_size, swap_partition_size)
