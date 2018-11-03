import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(config, root):
    if 'public_key' not in config:
        return

    authorized_keys_dir = os.path.join(root, "root/.ssh")
    authorized_keys_filename = os.path.join(authorized_keys_dir, "authorized_keys")
    # Adding the authorized keys
    if not os.path.exists(authorized_keys_dir):
        os.makedirs(authorized_keys_dir)
    with open(authorized_keys_filename, "a") as destination:
        destination.write(config['public_key'] + "\n")
    os.chmod(authorized_keys_filename, 0o600)

    sshd_config_filename = os.path.join(root, "etc/ssh/sshd_config")
    if os.path.exists(sshd_config_filename):
        # Change the sshd config to allow root login
        process = subprocess.Popen(["sed", "-i", "s/^\\s*PermitRootLogin\s\+no/PermitRootLogin yes/",
                                sshd_config_filename])
        return process.wait()
    else:
        return 0
