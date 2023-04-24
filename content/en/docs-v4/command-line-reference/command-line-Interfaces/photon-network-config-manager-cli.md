---
title:  Photon Network Config Manager Command-line Interface (nmctl)
weight: 3
---

For locally logged-on users, Photon OS provides a command line interface to manage network configuration of the system.

The network-config-manager `nmctl` allows to configure and introspect the state of the network links as seen by `systemd-networkd`. 

Query and control the netmanager subsystem.

     -h --help                    Show this help message and exit

     -v --version                 Show package version


    **Command                      Option                                    Description**


    show                                                                Show system status

    status                                                              List links

    status                       [LINK]                                 Show link status


    set-mtu                      [LINK] [MTU]                           Set Link MTU

    set-mac                      [LINK] [MAC]                           Set Link MAC 
 
    set-link-mode                [LINK] [MODE
                                 { yes | no | on | off | 1 | 0} ]       Set Link managed by networkd


    set-dhcp-mode                [LINK] [DHCP-MODE 
                                 { yes | no | ipv4 | ipv6 } ]            Set Link DHCP setting

    set-dhcp4-client-identifier  [LINK] [IDENTIFIER 
                                 { mac | duid | duid-only} ]


    set-dhcp-iaid                [LINK] [IAID]                            Sets the DHCP Identity Association Identifier
                                                                         (IAID) for the interface, a 32-bit unsigned
                                                                          integer.

    set-dhcp-duid                [LINK | system] [DUID 
                                 { link-layer-time | vendor 
                                 | link-layer | uuid } ] [RAWDATA]         Sets the DHCP Client 
                                                                           DUID type which specifies how the DUID 
                                                                            should be generated and [RAWDATA] to 
                                                                            overides the global DUIDRawData.


    set-link-state               [LINK] [STATE { up | down } ]              Set Link State

    add-link-address             [LINK] [ADDRESS] [PEER] ]                  Add Link Address

    delete-link-address          [LINK]                                     Removes Address from Link

    add-default-gateway          [LINK] [GW address] onlink 
                                 [ONLINK { yes | no | on | off | 1 | 0}]    Add Link Default Gateway

    delete-gateway               [LINK]                                     Removes Gateway from Link

    add-route                    [LINK] [GW address] metric 
                                 [METRIC { number }]                        Set Link route

    delete-route                 [LINK]                                     Removes route from Link

    add-additional-gw            [LINK] [ADDRESS] [ROUTE address] 
                                 [GW address] [ROUTING POLICY TABLE number] configures additional gateway for
						                                                    another NIC with routing policy rules

    set-hostname                 [HOSTNAME]                                  Sets hostname

    show-dns                                                                 Show DNS Servers

    add-dns                      [LINK | system] [ADDRESS]                   Set Link DNS servers

    add-domain                   [LINK | system] [DOMAIN]                     Set Link DOMAIN 

    show-domains                                                               Show DNS Server DOMAINS

    revert-resolve-link          [LINK]                                      Flushes all DNS server and Domain settings
                                                                               of the link

    set-link-local-address       [LINK] [LinkLocalAddressing 
                                 { yes | no | on | off | 1 | 0}]          Set Link link-local address autoconfiguration

    set-ipv4ll-route             [LINK] [IPv4LLRoute 
                                 { yes | no | on | off | 1 | 0}]           Set the route needed for non-IPv4LL hosts to
                                                                            communicate with IPv4LL-only hosts
          
                                      
    set-llmnr                    [LINK] [LLMNR 
                                 { yes | no | on | off | 1 | 0}]          Set Link Link-Local Multicast Name Resolution

    set-multicast-dns            [LINK] [MulticastDNS  
                                 { yes | no | on | off | 1 | 0}]            Set Link Multicast DNS

    set-lldp                     [LINK] [LLDP 
                                 { yes | no | on | off | 1 | 0}]           Set Link Ethernet LLDP packet reception

    set-emit-lldp                [LINK] [EmitLLDP 
                                 { yes | no | on | off | 1 | 0}]           Set Link Ethernet LLDP packet emission

    set-ipforward                [LINK] [IPForward 
                                 { yes | no | on | off | 1 | 0}]          Set Link IP packet forwarding for the system

    set-ipv6acceptra             [LINK] [IPv6AcceptRA 
                                 { yes | no | on | off | 1 | 0}]          Set Link IPv6 Router Advertisement (RA) 
                                                                          reception support for the interface

    set-ipmasquerade             [LINK] [IPMasquerade 
                                 { yes | no | on | off | 1 | 0}]          Set IP masquerading for the network interface

    set-dhcp4-use-dns            [LINK] [UseDNS 
                                 { yes | no | on | off | 1 | 0}]           Set Link DHCP4 Use DNS

    set-dhcp4-use-domains        [LINK] [UseDomains 
                                 { yes | no | on | off | 1 | 0}]            Set Link DHCP4 Use DOMAINS

    set-dhcp4-use-mtu            [LINK] [UseMTU 
                                 { yes | no | on | off | 1 | 0}]              Set Link DHCP4 Use MTU

    set-dhcp4-use-ntp            [LINK] [UseNTP 
                                 { yes | no | on | off | 1 | 0}]             Set Link DHCP4 Use NTP


    set-dhcp4-use-dns            [LINK] [UseDNS 
                                  { yes | no | on | off | 1 | 0}]            Set Link DHCP4 Use DNS


    set-dhcp6-use-dns            [LINK] [UseDNS 
                                 { yes | no | on | off | 1 | 0}]              Set Link DHCP6 Use DNS


    set-dhcp6-use-ntp            [LINK] [UseNTP 
                                 { yes | no | on | off | 1 | 0}]              Set Link DHCP6 Use NTP


    add-ntp                      [LINK] [NTP]                                 Add Link NTP server address. This option
                                                                              may be specified more than once.
                                                                              This setting is read by 
                                                                              systemd-timesyncd.service(8)


    set-ntp                      [LINK] [NTP]                                  Set Link NTP server address. This option
                                                                               may be specified more than once.
                                                                               This setting is read by 
                                                                               systemd-timesyncd.service(8)


    delete-ntp                   [LINK]                                          Delete Link NTP server addresses.
                                                                                 This setting is read by 
                                                                                 systemd-timesyncd.service(8)


    disable-ipv6                 [LINK]                                            Disables IPv6 on the interface.


    enable-ipv6                  [LINK]                                           Enables IPv6 on the interface.


    create-vlan                  [VLAN name] dev [LINK master] id [ID INTEGER]   Creates vlan netdev and sets master to
                                                                                 device


    create-bridge                [BRIDGE name] [LINK] [LINK] ...                 Creates bridge netdev and sets master
                                                                                 to device



    create-bond                  [BOND name] mode [MODE {balance-rr | 
                                 active-backup | balance-xor | broadcast         Creates bond netdev and sets master to
                                 | 802.3ad | balance-tlb | balance-alb}]         device
				                   [LINK] [LINK] ...       

                 
    create-vxlan                 [VXLAN name] [dev LINK] vni [INTEGER]        Creates vxlan VXLAN (Virtual eXtensible
                                 [local ADDRESS] [remote ADDRESS]             Local Area Network) tunneling.
                                 [port PORT] [independent 
                                 { yes | no | on | off | 1 | 0}]. 
				                                         
                                 
    create-macvlan               [MACVLAN name] dev [LINK] mode              Creates macvlan virtualized bridged
                                 [MODE {private | vepa | bridge | passthru    networking.
                                 | source}] 
                                       
                                  
    create-macvtap               [MACVTAP name] dev [LINK] mode              Creates macvtap virtualized bridged
                                 [MODE {private | vepa | bridge              networking.
                                 | passthru | source}]                    
                                                            
        
    create-ipvlan                [IPVLAN name] dev [LINK]                Creates ipvlan, virtual LAN, separates broadcast 
                                 mode [MODE {l2 | l3 | l3s}]             domains by adding tags to network packet.   


    create-ipvtap                [IPVTAP name] dev [LINK] 
                                 mode [MODE {l2 | l3 | l3s}]             Create ipvtap.


    create-vrf                   [VRF name] table [INTEGER}]            Creates Virtual routing and forwarding (VRF).


    create-veth                  [VETH name] peer [PEER name}]          Creates virtual Ethernet devices


    create-ipip                  [IPIP name] [dev LINK] 
                                 local [ADDRESS] remote [ADDRESS] 
                                 [independent 
                                 { yes | no | on | off | 1 | 0}]                  Creates ipip tunnel.


    create-sit                   [SIT name] [dev LINK] local 
                                 [ADDRESS] remote [ADDRESS] 
                                 [independent 
                                 { yes | no | on | off | 1 | 0}]                  Creates sit tunnel.


    create-vti                   [VTI name] [dev LINK] local [ADDRESS]
                                 remote [ADDRESS] [independent 
                                 { yes | no | on | off | 1 | 0}]                   Creates vti tunnel.


    create-gre                   [GRE name] [dev LINK] local [ADDRESS]
                                 remote [ADDRESS] [independent 
                                  { yes | no | on | off | 1 | 0}]                  Creates gre tunnel.


    create-wg                    [WIREGUARD name] private-key [PRIVATEKEY]
                                 listen-port [PORT INTEGER] public-key 
                                  [PUBLICKEY] preshared-key [PRESHAREDKEY]
						            allowed-ips [IP,IP ...] endpoint [IP:PORT]      Creates a wireguard tunnel.


    reload                                                                         Reload .network and .netdev files.

    reconfigure                   [LINK]                                           Reconfigure Link.


    generate-config-from-yaml     [FILE]                                           Generates network file configuration 
                                                                                   from yaml file.


    apply-yaml-config                                                              Generates network file configuration from
                                                                                   yaml files found in 
                                                                                   /etc/network-config-manager/yaml.


    generate-config-from-cmdline [FILE | COMMAND LINE]                            Generates network file configuration from 
                                                                                command kernel command line or command line.


    add-nft-table                [FAMILY {ipv4 | ipv6 | ip}] [TABLE]              adds a new table.

    show-nft-tables              [FAMILY {ipv4 | ipv6 | ip}]                      shows nftable's tables.


    delete-nft-table             [FAMILY {ipv4 | ipv6 | ip}] [TABLE]             deletes a existing nftable's table.


    add-nft-chain                [FAMILY {ipv4 | ip}] [TABLE] [CHAIN]               adds a new nftable's chain.


    show-nft-chains              [FAMILY {ipv4 | ipv6 | ip}] [TABLE]               shows nftable's chains.


    delete-nft-chain             [FAMILY {ipv4 | ipv6 | ip}] [TABLE] [CHAIN]       deletes a nftable's chain from table


    add-nft-rule                 [FAMILY {ipv4 | ipv6 | ip}] 
                                  [TABLE] [CHAIN] [PROTOCOL 
                                 { tcp | udp}] [SOURCE PORT / DESTINATION PORT
                                  {sport|dport}] PORT] [ACTION {accept | drop}]    configures a nft rule for a port.


    show-nft-rules               [TABLE]                                           shows nftable's rules.

    delete-nft-rule              [FAMILY {ipv4 | ipv6 | ip}] [TABLE] 
                                  [CHAIN] [HANDLE]                                 deletes a nftable's rule from table

    nft-run                                                                        runs a nft command.  See man NFT(8)