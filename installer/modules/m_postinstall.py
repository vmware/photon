import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config and 'postinstall' in ks_config:
        config['postinstall'] = ks_config['postinstall']
    if 'postinstall' not in config:
        return
    # run the script in the chroot environment
    script = config['postinstall']

    script_file = os.path.join(root, 'etc/tmpfiles.d/postinstall.sh')

    with open(script_file,  'wb') as outfile:
        outfile.write("\n".join(script))

    os.chmod(script_file, 0700);
    process = subprocess.Popen(["./mk-run-chroot.sh", '-w', root, "/etc/tmpfiles.d/postinstall.sh"])
    process.wait()
