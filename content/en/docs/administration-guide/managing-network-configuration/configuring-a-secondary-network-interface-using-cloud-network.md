---
title:  Configuring a Secondary Network Interface using Cloud-Network 
weight: 17
---

When you add a secondary network interface to a linux instance in the cloud environment, you need to configure the network parameters for the secondary interface in the linux instance. The configuration ensures that you do not face any routing issues while using the secondary network interface. Configuring the secondary network interface involves several manual processes that include configuring a new routing table, setting up rules in the routing table and so on.

`cloud-network` automates the whole manual process of configuring the secondary network interface. It configures the network parameters required for any network interfaces that you create or add to the linux instance. In a cloud environment, instances are set to public IPs and private IPs. If you add more than one private IP for the secondary network interface, the IP other than the one provided by DHCP cannot be fetched and configured for your virtual machine. The `cloud-network` project is designed to adapt the cloud-network environments such as Azure, GCP, and Amazon EC2. `cloud-network` fetches the metadata from the metadata server endpoint, parses the metadata, and then assigns IPs and routes. When `cloud-network` is installed, it automatically configures network interfaces in the cloud frameworks. It detects the available instances using netlink. Additionally, for all the interfaces, including the primary one, it looks for any secondary IP addresses from the metadata server endpoint and configures them on the interface, if any. 

A local RESTful JSON server runs on the address 127.0.0.1:5209 and the instance metadata is saved on per link basis in the following directory: `/run/cloud-network`.

The network parameters in the cloud framework are checked periodically for any changes, and in case of a change, the interface is reconfigured accordingly.

The image below illustrates the communication of `cloud-network` and the instance metadata server:

![Cloud Network tool communicating with the IMDS](/docs/images/Cloud-Network_and_Instance-Metadata-Service_Communication.jpg)


<br />

## Use Case: Making a secondary network interface work in a cloud instance. ##


This functionality is scattered across different scripts/tools that are cloud provider dependent. `cloud-network` provides a cloud-agnostic mechanism to retrieve the metadata like network parameters, and configure the interfaces. This means that there is no need to manually edit and update the configuration when there are changes in the network parameters. `cloud-network` automatically configures the interfaces since it has the metadata information.

The image below illustrates how `cloud-network` fetches the network parameters to configure the secondary network interface (eth1) in a cloud instance:

![Cloud Network tool configuring the secondary network instance](/docs/images/Secondary_Interface_Configuration.jpg)

<br />

## Installing Cloud Network Setup ##

Type the following command to install `cloud network` in your system:  

`tdnf install cloud-network-setup`

<br />

## Configuration ##

To manage the configuration, use the configuration file named `cloud-network.toml` located in the following directory: `/etc/cloud-network/`

### [System] Section ###
You can set values for the following keys in the `[System]` section:

`LogLevel=`  
Specifies the log level. The key takes one of the following values: `Trace`, `Debug`, `Info`, `Warning`, `Error`, `Fatal` and `Panic`. 
Default is `info`.

`LogFormat=`  
Specifies the log format. The key takes one of the following values:
text or JSON. Takes one of `text` or `json`, Default is `text`.

`RefreshTimer=`  
Specifies the time interval. The time interval indicates the amount of time taken to retrieve the data from the metadata endpoint.


### [Network] Section ###

You can set values for the following keys in the `[Network]` section:


`Address=`  
Specifies the IP address that the local REST API server listens. Default is `127.0.0.1`.

`Port=`  
Specifies the IP port that the local REST API server listens. Default is `5209`.

`Supplementary=`  
A whitespace-separated list of interfaces matching the device name. Specifies the interfaces you want to configure with a default gateway and routing policy rules for each IP address including the primary IP address. No default value is set for this key.

**Note** When there are multiple interfaces, the secondary interface becomes unreachable. When you set a value for `Supplementary=` key, the default route and routing policy rules are automatically configured. 

<br />

The following example shows a sample configuration of the key values in the `cloud-network.toml` file:


    > cat /etc/cloud-network/cloud-network.toml
    [System]
    RefreshTimer="300s"
    LogLevel="info"
    LogFormat="text"
    
    [Network]
    Address="127.0.0.1"
    Port="5209"
    Supplementary="ens3"


After you set the configuration, use the `sudo systemctl status cloud-network` command to check the network status of the `cloud-network` service. 
Following example shows the command output of the  `sudo systemctl status cloud-network` command:

    ❯ > sudo systemctl status cloud-network
    ● cloud-network.service - Configures network in cloud enviroment
         Loaded: loaded (/usr/lib/systemd/system/cloud-network.service; disabled; vendor preset: enabled)
         Active: active (running) since Mon 2021-05-31 22:54:50 UTC; 3min 31s ago
       Main PID: 19754 (cloud-network)
          Tasks: 5 (limit: 4400)
         Memory: 8.7M
         CGroup: /system.slice/cloud-network.service
                 └─19754 /usr/bin/cloud-network

    May 31 22:54:50 zeus-final-2 systemd[1]: Started Configures network in cloud enviroment.


<br />


## cnctl ##

Use the `cnctl` CLI tool to view the metadata that is retrieved from the endpoint metadata server. 
The Following examples show the output of the `cnctl status` command for the network and system:

    ❯ cnctl status system
        Cloud provider: aws
                 AmiID: ami-005f15863xxxxxxxx  
              Location: 0
    BlockDeviceMapping: Ami:xvda Root:/dev/xvda
              Hostname: Zeus.us-west-2.compute.internal
        PublicHostname: Zeuspublic.us-west-2.compute.amazonaws.com
         LocalHostname: Zeus.us-west-2.compute.internal
        InstanceAction: none
        InstanceID: i-0c8c1test
     InstanceLifeCycle: on-demand
          InstanceType: t4g.micro
             Placement: AvailabilityZone:us-west-2d AvailabilityZoneID:usw2-az4 Region:us-west-2
               Profile: default-hvm
           Mac Address: 0e:c5:3f:c5:33:a5
             LocalIpv4: 192.31.63.114
            PublicIpv4: 02:42:8d:4c:0c:cf
       Services Domain: amazonaws.com
    Services Partition: aws  

<br />


    ❯ cnctl status network
                Name: ens33
         MAC Address: 00:0c:29:5f:d1:39
           Public IP: 104.42.20.194
          Private IP: 10.0.0.4/24 10.0.0.6/24 10.0.0.7/24
              Subnet: 10.0.0.0




