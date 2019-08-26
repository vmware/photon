import os
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    # Set locale
    with open(os.path.join(installer.photon_root, "etc/locale.conf"), "w") as locale_conf:
        locale_conf.write("LANG=en_US.UTF-8\n")

    #locale-gen.sh needs /usr/share/locale/locale.alias which is shipped with
    #  glibc-lang rpm, in some photon installations glibc-lang rpm is not installed
    #  by default. Call localedef directly here to define locale environment.
    installer.cmd.run_in_chroot(installer.photon_root, "/usr/bin/localedef -c -i en_US -f UTF-8 en_US.UTF-8")

