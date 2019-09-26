import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    if 'postinstall' not in installer.install_config:
        return

    installer.logger.info("Run postinstall script")
    # run the script in the chroot environment
    script = installer.install_config['postinstall']

    script_file = os.path.join(installer.photon_root, 'etc/tmpfiles.d/postinstall.sh')

    with open(script_file, 'wb') as outfile:
        outfile.write("\n".join(script).encode())

    os.chmod(script_file, 0o700)
    return installer.cmd.run(["./mk-run-chroot.sh", '-w', installer.photon_root,
                              "/etc/tmpfiles.d/postinstall.sh"]) == 0
