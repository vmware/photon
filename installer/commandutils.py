# pylint: disable=invalid-name,missing-docstring
import subprocess
import os
import crypt
import string
import random
import shutil
import ssl
import requests
from urllib.parse import urlparse
from OpenSSL.crypto import load_certificate, FILETYPE_PEM

class CommandUtils(object):
    def __init__(self, logger):
        self.logger = logger

    def run(self, cmd):
        self.logger.debug(cmd)
        use_shell = not isinstance(cmd, list)
        process = subprocess.Popen(cmd, shell=use_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = process.communicate()
        retval = process.returncode
        if out != b'':
            self.logger.info(out.decode())
        if retval != 0:
            self.logger.info("Command failed: {}".format(cmd))
            self.logger.info("Error code: {}".format(retval))
            self.logger.error(err.decode())
        return retval

    def run_in_chroot(self, chroot_path, cmd):
        # Use short command here. Initial version was:
        # chroot "${BUILDROOT}" \
        #   /usr/bin/env -i \
        #   HOME=/root \
        #   TERM="$TERM" \
        #   PS1='\u:\w\$ ' \
        #   PATH=/bin:/usr/bin:/sbin:/usr/sbin \
        #   /usr/bin/bash --login +h -c "cd installer;$*"
        return self.run(['chroot', chroot_path, '/bin/bash', '-c', cmd])

    @staticmethod
    def is_vmware_virtualization():
        """Detect vmware vm"""
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        return out.decode() == 'vmware\n'

    @staticmethod
    def generate_password_hash(password):
        """Generate hash for the password"""
        shadow_password = crypt.crypt(
            password, "$6$" + "".join(
                [random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    @staticmethod
    def _requests_get(url, verify):
        try:
            r = requests.get(url, verify=verify, stream=True, timeout=5.0)
        except:
            return None
        return r

    @staticmethod
    def wget(url, out, enforce_https=True, ask_fn=None, fingerprint=None):
        # Check URL
        try:
            u = urlparse(url)
        except:
            return False, "Failed to parse URL"
        if not all([ u.scheme, u.netloc ]):
            return False, 'Invalid URL'
        if enforce_https:
            if u.scheme != 'https':
                return False, 'URL must be of secure origin (HTTPS)'
        r = CommandUtils._requests_get(url, True)
        if r is None:
            if fingerprint is None and ask_fn is None:
                return False, "Unable to verify server certificate"
            port = u.port
            if port is None:
                port = 443
            try:
                pem = ssl.get_server_certificate((u.netloc, port))
                cert = load_certificate(FILETYPE_PEM, pem)
                fp = cert.digest('sha1').decode()
            except:
                return False, "Failed to get server certificate"
            if ask_fn is not None:
                if not ask_fn(fp):
                    return False, "Aborted on user request"
            else:
                if fingerprint != fp:
                    return False, "Server fingerprint did not match provided. Got: " + fp
            # Download file without validation
            r = CommandUtils._requests_get(url, False)
            if r is None:
                return False, "Failed to download file"
        r.raw.decode_content = True
        with open(out, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return True, None
