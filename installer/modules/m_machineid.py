import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    # Generage machine-id for live setup, but keep this file empty for images
    # so it gets regenerated on boot.
    if installer.install_config['live']:
        installer.cmd.run_in_chroot(installer.photon_root, "/bin/systemd-machine-id-setup")
    else:
        open(installer.photon_root + "/etc/machine-id", "w").close()

