#
#            © 2019 VMware Inc.,
#
#     Date: Fri Aug 30 11:28:18 IST 2019
#   Author: Ankit Jain <ankitja@vmware.com>

import random
from networkmanager import NetworkManager
from menu import Menu
from window import Window
from windowstringreader import WindowStringReader
from readmultext import ReadMulText
from actionresult import ActionResult

class NetworkConfigure(object):

    NET_CONFIG_OPTION_DHCP = 0
    NET_CONFIG_OPTION_DHCP_HOSTNAME = 1
    NET_CONFIG_OPTION_MANUAL = 2
    NET_CONFIG_OPTION_VLAN = 3

    NET_CONFIG_OPTION_STRINGS = [
        "Configure network automatically",
        "Configure network automatically with a DHCP hostname",
        "Configure network manually",
        "Configure network using VLAN",
    ]

    VLAN_READ_STRING = (
        'IEEE 802.1Q Virtual LANs (VLANs) are a way of partitioning a physical network '
        'into distinct broadcast domains. Packets can be tagged with different VLAN IDs '
        'so that a single "trunk" connection may be used to transport data for various VLANs.\n'
        '\n'
        'If the network interface is directly connected to a VLAN trunk port,\n'
        'specifying a VLAN ID may be necessary to get a working connection.\n'
        '\n'
        'VLAN ID (1-4094): '
    )

    def __init__(self, maxy, maxx, install_config):
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 80
        self.win_height = 13
        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2
        self.menu_starty = self.win_starty + 3
        self.package_menu_items = []
        self.install_config = install_config
        self.install_config['network'] = {}

        for opt in self.NET_CONFIG_OPTION_STRINGS:
            self.package_menu_items.append((opt, self.exit_function, [opt]))
        self.package_menu = Menu(self.menu_starty, self.maxx, self.package_menu_items,
                                 default_selected=0, tab_enable=False)
        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Network Configuration', True, action_panel=self.package_menu,
                             can_go_next=True, position=1)

    @staticmethod
    def validate_hostname(hostname):
        if hostname is None or len(hostname) == 0:
            return False, "Empty hostname or domain is not allowed"

        fields = hostname.split('.')
        for field in fields:
            if not field:
                return False, "Empty hostname or domain is not allowed"
            if field[0] == '-' or field[-1] == '-':
                return False, "Hostname or domain should not start or end with '-'"

        machinename = fields[0]
        if len(machinename) > 64 or not machinename[0].isalpha():
            return False, "Hostname should start with alpha char and <= 64 chars"

        return True, None

    @staticmethod
    def validate_ipaddr(ip, can_have_cidr=False):
        if ip is None or len(ip) == 0:
            return False, "IP address cannot be empty"

        cidr = None
        if can_have_cidr and '/' in ip:
            ip, cidr = ip.split('/')

        octets = ip.split('.')
        if len(octets) != 4:
            return False, "Invalid IP; Must be of the form: xxx.xxx.xxx.xxx"

        for octet in octets:
            if not octet or not octet.isdigit() or ((int(octet) < 0) or (int(octet) > 255)):
                return False, "Invalid IP; Digit should be between (0 <= x <= 255)"

        if cidr is not None:
            if not cidr.isdigit() or int(cidr) >= 32 or int(cidr) <= 0:
                return False, "Invalid CIDR number!"

        return True, None

    def validate_static_conf(self, vals):
        for val in vals:
            res, msg = self.validate_ipaddr(val)
            if not res:
                return res, msg
        return True, None

    @staticmethod
    def validate_vlan_id(vlan_id):
        if vlan_id is None or not vlan_id:
            return False, 'Empty VLAN ID is not allowed !!'

        if ((int(vlan_id) < 1) or (int(vlan_id) > 4094)):
            return False, 'Incorrect VLAN ID !! Digit should be between (1 <= x <= 4094)'

        return True, None

    def exit_function(self, selected_item_params):
        selection = self.NET_CONFIG_OPTION_STRINGS.index(selected_item_params[0])

        if selection == self.NET_CONFIG_OPTION_DHCP:
            self.install_config['network']['type'] = 'dhcp'

        elif selection == self.NET_CONFIG_OPTION_DHCP_HOSTNAME:
            network_config = {}
            random_id = '%12x' % random.randrange(16**12)
            random_hostname = 'photon-' + random_id.strip()
            accepted_chars = list(range(ord('A'), ord('Z')+1))
            accepted_chars = list(range(ord('a'), ord('z')+1))
            accepted_chars.extend(range(ord('0'), ord('9')+1))
            accepted_chars.extend([ord('.'), ord('-')])
            result = WindowStringReader(self.maxy, self.maxx, 13, 80, 'hostname', None, None,
                                        accepted_chars, NetworkConfigure.validate_hostname,
                                        None, 'Choose the DHCP hostname for your system',
                                        'DHCP Hostname:', 2, network_config, random_hostname,
                                        True).get_user_string(None)
            if not result.success:
                return ActionResult(False, {'custom': False})

            self.install_config['network'] = network_config
            self.install_config['network']['type'] = 'dhcp'

        elif selection == self.NET_CONFIG_OPTION_MANUAL:
            network_config = {}
            items = [ 'IP Address', 'Netmask', 'Gateway', 'Nameserver' ]
            keys =  [ 'ip_addr',    'netmask', 'gateway', 'nameserver' ]
            self.create_window = ReadMulText(self.maxy, self.maxx, 0, network_config,
                                             '_conf_', items, None, None, None,
                                              self.validate_static_conf, None, True)
            result = self.create_window.do_action()
            if not result.success:
                return ActionResult(False, {'goBack': True})

            for i in range(len(items)):
                network_config[keys[i]] = network_config.pop('_conf_' + str(i), None)
            self.install_config['network'] = network_config
            self.install_config['network']['type'] = 'static'

        elif selection == self.NET_CONFIG_OPTION_VLAN:
            network_config = {}
            result = WindowStringReader(self.maxy, self.maxx, 18, 75, 'vlan_id', None,
                                        None, list(range(48, 58)), NetworkConfigure.validate_vlan_id,
                                        None, '[!] Configure the network', self.VLAN_READ_STRING,
                                        6, network_config, '', True).get_user_string(True)

            if not result.success:
                return ActionResult(False, {'goBack': True})

            self.install_config['network'] = network_config
            self.install_config['network']['type'] = 'vlan'

        return ActionResult(True, {'custom': False})

    def display(self):
        return self.window.do_action()
