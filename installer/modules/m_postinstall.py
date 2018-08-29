import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(config, root):
    if 'postinstall' not in config:
        return
    # run the script in the chroot environment
    script = config['postinstall']

    script_file = os.path.join(root, 'etc/tmpfiles.d/postinstall.sh')

    with open(script_file, 'wb') as outfile:
        outfile.write("\n".join(script).encode())

    os.chmod(script_file, 0o700)
    with open(commons.KS_POST_INSTALL_LOG_FILE_NAME, "w") as logfile:
        process = subprocess.Popen(["./mk-run-chroot.sh", '-w', root,
                                    "/etc/tmpfiles.d/postinstall.sh"],
                                   stdout=logfile, stderr=logfile)
        retval = process.wait()
        if retval == 0:
            return True
        return False
