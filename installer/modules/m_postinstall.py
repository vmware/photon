import os
import subprocess
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    if 'postinstall' not in installer.install_config or 'postinstallscripts' not in installer.install_config:
        return

    tempdir = "/tmp/tempscripts"
    tempdir_full = installer.photon_root + tempdir
    if not os.path.exists(tempdir_full):
        os.mkdir(tempdir_full)

    if 'postinstall' in installer.install_config:
        installer.logger.info("Run postinstall script")
        # run the script in the chroot environment
        script = installer.install_config['postinstall']

        script_file = os.path.join(tempdir_full, 'builtin_postinstall.sh')

        with open(script_file, 'wb') as outfile:
            outfile.write("\n".join(script).encode())
        os.chmod(script_file, 0o700)

    if 'postinstallscripts' in installer.install_config:
        for scriptname in config['postinstallscripts']:
            script_file = installer.getfile(scriptname)
            shutil.copy(script_file, tempdir_full)

    for script in os.listdir(tempdir_full):
        installer.logger.info("Running script {}".format(script))
        installer.cmd.run_in_chroot(installer.photon_root, "{}/{}".format(tempdir, script))

    shutil.rmtree(tempdir_full, ignore_errors=True)
