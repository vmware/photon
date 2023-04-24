---
title:  Examining the Packages in the SPECS Directory on Github
weight: 1
---

The SPECS directory of the GitHub website for Photon OS contains all the packages that can appear in Photon OS repositories. The following is the path to the SPECS directory:  

`https://github.com/vmware/photon/tree/master/SPECS`

To see the version of a package, in the SPECS directory, click the name of the subdirectory of the package that you want to examine, and then click the `.spec` filename in the subdirectory. 

For example, `python3.spec` appears as follows::

```
%global VER 3.11
%global with_gdb_hooks 1

Summary:        A high-level scripting language
Name:           python3
Version:        3.11.0
Release:        6%{?dist}
License:        PSF
URL:            http://www.python.org
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
```


