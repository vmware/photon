#
#            (c) 2019 VMware Inc.,
#
#     Date: Fri Aug 30 11:28:18 IST 2019
#   Author: Siddharth Chandrasekaran <csiddharth@vmware.com>

import os
import subprocess
import shutil

class NetworkManager():

    TEMPLATE_NET_DHCP = (
        '[Match]\n'
        'Name=e*\n'
        '\n'
        '[Network]\n'
        'DHCP=yes\n'
        'IPv6AcceptRA=no\n'
    )

    TEMPLATE_NET_STATIC = (
        "[Match]\n"
        "Name=eth0\n"
        "\n"
        "[Network]\n"
        "Address=@IP_ADDR@\n"
        "Gateway=@GATEWAY@\n"
        "DNS=@DNS@\n"
    )

    TEMPLATE_NET_DHCP_HOSTNAME = (
        "\n"
        "[DHCP]\n"
        "SendHostname=True\n"
        "Hostname=@HOSTNAME@\n"
    )

    TEMPLATE_NET_VLAN_NETDEV = (
        '[NetDev]\n'
        'Name=eth0.@VLAN_NO@\n'
        'Kind=vlan\n'
        '\n'
        '[VLAN]\n'
        'Id=@VLAN_NO@\n'
    )

    TEMPLATE_NET_VLAN_NETWORK = (
        '[Match]\n'
        'Name=eth0.@VLAN_NO@\n'
        '\n'
        '[Network]\n'
        'DHCP=yes\n'
        'IPv6AcceptRA=no\n'
    )

    def __init__(self, install_config, photon_root='/'):
        self.photon_root = photon_root
        self.install_config = install_config
        # Installed system config directory (keep - persistent)
        self.conf_dir = os.path.join(self.photon_root, 'etc/systemd/network')

        # Get contents of default dhcp config.
        filename = '/etc/systemd/network/99-dhcp-en.network'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.TEMPLATE_NET_DHCP = f.read()
                self.TEMPLATE_NET_DHCP += '\n\n'

    def rm_f(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)

    def clean_conf_files(self):
        if 'conf_files' not in self.install_config['network']:
            return
        for filename in self.install_config['network']['conf_files']:
            self.rm_f(filename)
        self.install_config['network']['conf_files'] = []

    def netmask_to_cidr(self, netmask):
        # param: netmask ip addr (eg: 255.255.255.0)
        # return: equivalent cidr number to given netmask ip (eg: 24)
        return sum([bin(int(x)).count('1') for x in netmask.split('.')])

    def exec_cmd(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        retval = process.wait()
        if retval != 0:
            return False
        return True

    def restart_networkd(self):
        if not self.exec_cmd('systemctl restart systemd-networkd'):
            raise Exception('Failed to restart networkd')

    def setup_network(self):
        if 'type' not in self.install_config['network']:
            return False
        if self.install_config['network']['type'] == 'dhcp':
            return self.setup_network_dhcp()
        elif self.install_config['network']['type'] == 'static':
            return self.setup_network_static()
        elif self.install_config['network']['type'] == 'vlan':
            return self.setup_network_vlan()
        return False

    def setup_network_dhcp(self):
        self.install_config['network']['type'] = 'dhcp'
        self.install_config['network']['conf_files'] = []
        hostname = self.install_config['network'].get('hostname', None)

        filename = os.path.join(self.conf_dir, '99-dhcp-en.network')
        with open(filename, 'w') as f:
            f.write(self.TEMPLATE_NET_DHCP)
            if hostname is not None:
                f.write(self.TEMPLATE_NET_DHCP_HOSTNAME.replace('@HOSTNAME@', hostname))
        self.install_config['network']['conf_files'].append(filename)

        # Add a hosts entry
        if hostname is not None:
            hosts_file = os.path.join(self.photon_root, '/etc/hosts')
            with open(hosts_file, 'a') as f:
                f.write('\n127.0.0.1 {}\n'.format(hostname))

        return True

    def setup_network_static(self):
        if ('ip_addr' not in self.install_config['network'] or
                'netmask' not in self.install_config['network'] or
                'gateway' not in self.install_config['network'] or
                'nameserver' not in self.install_config['network']):
            return False

        self.install_config['network']['type'] = 'static'
        self.install_config['network']['conf_files'] = []

        if ('/' not in self.install_config['network']['ip_addr'] and
                'netmask' in self.install_config['network']):
            cidr = self.netmask_to_cidr(self.install_config['network']['netmask'])
            self.install_config['network']['ip_addr'] += '/' + str(cidr)
            self.install_config['network'].pop('netmask')

        s = self.TEMPLATE_NET_STATIC
        s = s.replace('@IP_ADDR@', self.install_config['network']['ip_addr'])
        s = s.replace('@GATEWAY@', self.install_config['network']['gateway'])
        s = s.replace('@DNS@', self.install_config['network']['nameserver'])

        filename = os.path.join(self.conf_dir, '99-static-en.network')
        with open(filename, 'w') as f:
            f.write(s)
        self.install_config['network']['conf_files'].append(filename)

        return True

    def setup_network_vlan(self):
        if 'vlan_id' not in self.install_config['network']:
            return False
        self.install_config['network']['type'] = 'vlan'
        self.install_config['network']['conf_files'] = []
        vlan = self.install_config['network']['vlan_id']

        filename = os.path.join(self.conf_dir, '99-dhcp-en.network')
        with open(filename, 'w') as f:
            f.write(self.TEMPLATE_NET_DHCP)
            f.write('VLAN=eth0.{}\n'.format(str(vlan)))
        self.install_config['network']['conf_files'].append(filename)

        filename = '99-dhcp-en.vlan_' + vlan + '.netdev'
        filename = os.path.join(self.conf_dir, filename)
        with open(filename, 'w') as f:
            f.write(self.TEMPLATE_NET_VLAN_NETDEV.replace('@VLAN_NO@', str(vlan)))
        self.install_config['network']['conf_files'].append(filename)

        filename = '99-dhcp-en.vlan_' + vlan + '.network'
        filename = os.path.join(self.conf_dir, filename)
        with open(filename, 'w') as f:
            f.write(self.TEMPLATE_NET_VLAN_NETWORK.replace('@VLAN_NO@', str(vlan)))
        self.install_config['network']['conf_files'].append(filename)

        return True

    def teardown_network_config(self):
        self.clean_conf_files()
        self.install_config['network'].pop('type', None)

        # clean the hosts file entry
        if 'hostname' in self.install_config['network']:
            hosts_file = os.path.join(self.photon_root, '/etc/hosts')
            with open(hosts_file, 'r') as f:
                lines = f.readlines()
            with open(hosts_file, 'w') as f:
                for line in lines:
                    if self.install_config['network']['hostname'] not in line:
                        f.write(line)
            self.install_config['network'].pop('hostname', None)
