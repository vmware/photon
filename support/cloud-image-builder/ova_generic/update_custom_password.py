#!/usr/bin/python2

import os
import crypt
import random
import string
import sys
import re


def crypt_password(password, root_path):
    shadow_password = crypt.crypt(password, "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))

    shadow_filename = os.path.join(root_path, 'etc/shadow')
    
    if os.path.isfile(shadow_filename) == False:
        with open(shadow_filename, "w") as destination:
            destination.write("root:"+shadow_password+":")
    else:
        #add password hash in shadow file
        with open(shadow_filename, "r") as source:
            lines=source.readlines()

        with open(shadow_filename, "w") as destination:
            for line in lines:
                destination.write(re.sub("root:x:",  "root:"+shadow_password+":",  line))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage : update_custom_password.py <password> <root_path>")
        sys.exit(1)
    crypt_password(str(sys.argv[1]), str(sys.argv[2]))
