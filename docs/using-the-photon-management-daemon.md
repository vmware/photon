# Using the Photon Management Daemon

The Photon Management Daemon (PMD) that ships with Photon OS 2.0 provides the remote management of a Photon instance via several APIs: a command line client (pmd-cli), a REST API, and a Python API. The PMD provides the ability to manage network interfaces, packages, firewalls, users, and user groups.

## Installing the pmd Package

The pmd package is included with your Photon OS 2.0 distribution. To make sure that you have the latest version, you can run:
~~~~
# tdnf install pmd
# systemctl start pmd
~~~~
## Available APIs

### pmd-cli

The pmd-cli utility enables Photon customers to invoke API requests securely on local and remote servers. For details, see [Photon Management Daemon Command-line Interface (pmd-cli)](pmd-cli.md).

### PMD REST API

The PMD REST API is an openapi 2.0 specification. Once the pmd package is installed, you can use a Swagger UI tool to browse the REST API specifications (/etc/pmd/restapispec.json).
You can also browse it using the copenapi_cli tool that comes with the pmd package:
~~~~
# copenapi_cli --apispec /etc/pmd/restapispec.json
~~~~
For more information about the copenapi_cli tool, refer to [github.com/vmware/copenapi](https://github.com/vmware/copenapi).

### PMD Python API

Python3 is included with your Photon OS 2.0 distribution. PMD Python interfaces are available for python3 (pmd-python3) and python2 (pmd-python2). You can use tdnf to ensure that the latest version is installed:
~~~~
# tdnf install pmd-python3
# systemctl start pmd
~~~~
To navigate the help documentation for the pmd Python packages:
~~~~
# python3
>>> import pmd
>>> net = pmd.server().net
>>> help(pmd)
~~~~
To show help text for individual interfaces:
~~~~
>>> help(pmd.server().net)
>>> help(pmd.server().pkg)
>>> help(pmd.server().firewall)
>>> help(pmd.server().user)
~~~~
For details about the network commands, see also the [Network Configuration Manager - Python API](netmgr.python.md).

### PMD C Documentation

PMD C APIs are defined in the header files (pmd_fwmgmt.h, pmd_netmgr.h, pmd_pkgmgmt.h, pmd_usermgmt.h) that are stored in the following location:  
~~~~
[https://github.com/vmware/pmd/tree/master/include](https://github.com/vmware/pmd/tree/master/include)
~~~~
For details about the network commands, see also the [Network Configuration Manager - C API](netmgr.c.md).
