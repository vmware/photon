import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    if 'public_key' not in installer.install_config:
        return

    authorized_keys_dir = os.path.join(installer.photon_root, "root/.ssh")
    authorized_keys_filename = os.path.join(authorized_keys_dir, "authorized_keys")
    sshd_config_filename = os.path.join(installer.photon_root, "etc/ssh/sshd_config")

    # Adding the authorized keys
    if not os.path.exists(authorized_keys_dir):
        os.makedirs(authorized_keys_dir)
    with open(authorized_keys_filename, "a") as destination:
        destination.write(installer.install_config['public_key'] + "\n")
    os.chmod(authorized_keys_filename, 0o600)

    # Change the sshd config to allow root login
    return installer.cmd.run(["sed", "-i", "s/^\\s*PermitRootLogin\s\+no/PermitRootLogin yes/",
                                sshd_config_filename]) == 0
