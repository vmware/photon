import os
import commons
import random

install_phase = commons.POST_INSTALL
enabled = True

def execute(name, config, root):
    hostname = config['hostname']

    hostname_file = os.path.join(root, 'etc/hostname')
    hosts_file    = os.path.join(root, 'etc/hosts')

    with open(hostname_file, 'w') as outfile:
        outfile.write(hostname)

    pattern = r'(127\.0\.0\.1)(\s+)(localhost)\s*\Z'
    replace = r'\1\2\3\n\1\2' + hostname
    commons.replace_string_in_file(hosts_file, pattern, replace)
