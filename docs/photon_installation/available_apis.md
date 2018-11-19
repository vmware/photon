# Available APIs

Photon OS includes the following APIs:

- PMD Rest API
- PMD Python API
- PMD C API

## PMD REST API

The PMD REST API is an openapi 2.0 specification. Once the pmd package is installed, you can use a Swagger UI tool to browse the REST API specifications (/etc/pmd/restapispec.json).
You can also browse it using the copenapi_cli tool that comes with the pmd package:
~~~~
# copenapi_cli --apispec /etc/pmd/restapispec.json
~~~~
For more information about the copenapi_cli tool, refer to [github.com/vmware/copenapi](https://github.com/vmware/copenapi).

## PMD Python API

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
For details about the network commands, see also the [Network Configuration Manager - Python API](photon_admin/netmgr.python.md).

## PMD C API

PMD C APIs are defined in the header files (pmd_fwmgmt.h, pmd_netmgr.h, pmd_pkgmgmt.h, pmd_usermgmt.h) that are stored in the following location:  
~~~~
[https://github.com/vmware/pmd/tree/master/include](https://github.com/vmware/pmd/tree/master/include)
~~~~
For details about the network commands, see also the [Network Configuration Manager - C API](photon_admin/netmgr.c.md).