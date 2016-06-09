import os
import subprocess
import commons

install_phase = commons.PRE_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config:
        if 'partitions' in ks_config:
            partitions = ks_config['partitions']
        else:
            partitions = commons.default_partitions
        config['disk'] = commons.partition_disk(ks_config['disk'], partitions)
