import os
import commons
from jsonwrapper import JsonWrapper

install_phase = commons.PRE_INSTALL
enabled = True

def get_packages_to_install(options, config_type):
        package_list = []
        install_option = options[config_type]
        for include_type in install_option["include"]:
            package_list = package_list + get_packages_to_install(options, include_type)
        json_wrapper_package_list = JsonWrapper(install_option["file"])
        package_list_json = json_wrapper_package_list.read()
        package_list = package_list + package_list_json["packages"]

        return package_list

def execute(name, ks_config, config, root):

    if ks_config:

        options = JsonWrapper("build_install_options_all.json").read()
        packages = get_packages_to_install(options, ks_config['type'])

        if 'additional_packages' in ks_config:
            packages.extend(ks_config['additional_packages'])

        config['type'] = ks_config['type']
        config["packages"] = packages
