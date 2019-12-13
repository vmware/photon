import os
import crypt
import random
import string
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(installer):
    shadow_password = installer.install_config['shadow_password']
    installer.logger.info("Set root password")

    passwd_filename = os.path.join(installer.photon_root, 'etc/passwd')
    shadow_filename = os.path.join(installer.photon_root, 'etc/shadow')

    #replace root blank password in passwd file to point to shadow file
    commons.replace_string_in_file(passwd_filename, "root::", "root:x:")

    if os.path.isfile(shadow_filename) == False:
        with open(shadow_filename, "w") as destination:
            destination.write("root:" + shadow_password + ":")
    else:
        #add password hash in shadow file
        commons.replace_string_in_file(shadow_filename, "root::", "root:"+shadow_password+":")
        commons.replace_string_in_file(shadow_filename, "root:x:", "root:"+shadow_password+":")

    installer.cmd.run_in_chroot(installer.photon_root, "/usr/sbin/pwconv")
    installer.cmd.run_in_chroot(installer.photon_root, "/usr/sbin/grpconv")

    if 'age' in installer.install_config.get('password', {}):
        age = installer.install_config['password']['age']
        login_defs_filename = os.path.join(installer.photon_root, 'etc/login.defs')

        # Do not run 'chroot -R' from outside. It will not find nscd socket.
        if age == -1:
            installer.cmd.run_in_chroot(installer.photon_root, "chage -I -1 -m 0 -M 99999 -E -1 -W 7 root")
            commons.replace_string_in_file(login_defs_filename, r'(PASS_MAX_DAYS)\s+\d+\s*', 'PASS_MAX_DAYS\t99999\n')
        elif age == 0:
            installer.cmd.run_in_chroot(installer.photon_root, "chage -d 0 root")
        else:
            installer.cmd.run_in_chroot(installer.photon_root, "chage -M {} root".format(age))
            commons.replace_string_in_file(login_defs_filename, r'(PASS_MAX_DAYS)\s+\d+\s*', 'PASS_MAX_DAYS\t{}\n'.format(age))

