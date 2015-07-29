import os
import commons
import crypt
import random
import string

install_phase = commons.POST_INSTALL
enabled = True

def execute(name, ks_config, config, root):

    if ks_config:
        # crypt the password if needed
        if ks_config['password']['crypted']:
            config['password'] = ks_config['password']['text']
        else:
            config['password'] = crypt.crypt(ks_config['password']['text'], 
                "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
    
    shadow_password = config['password']

    passwd_filename = os.path.join(root, 'etc/passwd')
    shadow_filename = os.path.join(root, 'etc/shadow')
    
    #replace root blank password in passwd file to point to shadow file
    commons.replace_string_in_file(passwd_filename,  "root::", "root:x:")

    if os.path.isfile(shadow_filename) == False:
        with open(shadow_filename, "w") as destination:
            destination.write("root:"+shadow_password+":")
    else:
        #add password hash in shadow file
        commons.replace_string_in_file(shadow_filename, "root::", "root:"+shadow_password+":")
        commons.replace_string_in_file(shadow_filename, "root:x:", "root:"+shadow_password+":")

