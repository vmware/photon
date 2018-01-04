import os
import crypt
import random
import string
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(config, root):
    shadow_password = config['password']

    passwd_filename = os.path.join(root, 'etc/passwd')
    shadow_filename = os.path.join(root, 'etc/shadow')

    #replace root blank password in passwd file to point to shadow file
    commons.replace_string_in_file(passwd_filename, "root::", "root:x:")

    if os.path.isfile(shadow_filename) == False:
        with open(shadow_filename, "w") as destination:
            destination.write("root:" + shadow_password + ":")
    else:
        #add password hash in shadow file
        commons.replace_string_in_file(shadow_filename, "root::", "root:"+shadow_password+":")
        commons.replace_string_in_file(shadow_filename, "root:x:", "root:"+shadow_password+":")
