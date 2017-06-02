import os
import commons
import random

install_phase = commons.POST_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config:
        if "hostname" in ks_config:
            evalhostname = os.popen('printf ' + ks_config["hostname"].strip(" ")).readlines()
            config['hostname'] = evalhostname[0]
        if "hostname" not in config or config['hostname'] == "":
            random_id = '%12x' % random.randrange(16**12)
            config['hostname'] = "photon-" + random_id.strip()

    hostname = config['hostname']

    hostname_file = os.path.join(root, 'etc/hostname')
    hosts_file = os.path.join(root, 'etc/hosts')

    with open(hostname_file,  'wb') as outfile:
        outfile.write(hostname)

    commons.replace_string_in_file(hosts_file, r'127\.0\.0\.1\s+localhost\s*\Z', '127.0.0.1\tlocalhost\n127.0.0.1\t' + hostname)
