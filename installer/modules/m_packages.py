import os
import commons
from jsonwrapper import JsonWrapper

install_phase = commons.PRE_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config:
        package_list = JsonWrapper("package_list.json").read()

        if ks_config['type'] == 'micro':
            packages = package_list["micro_packages"]
        elif ks_config['type'] == 'minimal':
            packages = package_list["minimal_packages"]
        elif ks_config['type'] == 'full':
            packages = package_list["minimal_packages"] + package_list["optional_packages"]
        else:
            #TODO: error
            packages = []

        config['type'] = ks_config['type']        
        config["packages"] = packages
