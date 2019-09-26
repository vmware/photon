import os
import random
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    hostname = installer.install_config['hostname']

    installer.logger.info("Set /etc/hostname to " + hostname)
    hostname_file = os.path.join(installer.photon_root, 'etc/hostname')
    hosts_file    = os.path.join(installer.photon_root, 'etc/hosts')

    with open(hostname_file, 'wb') as outfile:
        outfile.write(hostname.encode())

    pattern = r'(127\.0\.0\.1)(\s+)(localhost)\s*\Z'
    replace = r'\1\2\3\n\1\2' + hostname
    commons.replace_string_in_file(hosts_file, pattern, replace)
