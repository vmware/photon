import os
import commons
from jsonwrapper import JsonWrapper

install_phase = commons.PRE_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config:
        package_list_micro = JsonWrapper("packages_micro.json").read()
        package_list_minimal = JsonWrapper("packages_minimal.json").read()
        package_list_full = JsonWrapper("packages_full.json").read()

        if ks_config['type'] == 'micro':
            packages = package_list_micro["packages"]
        elif ks_config['type'] == 'minimal':
            packages = package_list_minimal["packages"]
        elif ks_config['type'] == 'full':
            packages = package_list_minimal["packages"] + package_list_full["packages"]
        else:
            #TODO: error
            packages = []

        config['type'] = ks_config['type']
        config["packages"] = packages
