---
title:  Prerequisites for Running Photon OS on vSphere
weight: 1
---

Resource requirements and recommendations vary depending on several factors, including the VMware vSphere host environment, the distribution file used (ISO or OVA) and the selected installation settings.

Before you use Photon OS within VMware vSphere, perform the following prerequisite tasks:

1. Verify that you have the following resources:

	<table style="height: 170px;" border="1" width="auto" cellspacing="0" cellpadding="10">
	<tbody>
	<tr>
	<td><b>Resource</b></td>
	<td><b>Description</b></td>
	</tr>
	<tr>
	<td> VMware vSphere installed</td>
	<td> Use vSphere client or ESXi host client </td>
	</tr>
	<tr>
	<td>Memory</td>
	<td>ESXi host with at least 1GB of free RAM (minimum)</td>
	</tr>
	<tr>
	<td>Storage</td>
	<td><b>Minimal Photon install</b>: ESXi host with at least 1GB of free space (minimum)<p><b>Full Photon install</b>: ESXi host with at least 4GB of free space (minimum), 16GB is recommended</p></td>
	</tr>
	<tr>
	<td>Distribution File</td>
	<td>Photon OS ISO or OVA file downloaded from <a href="https://github.com/vmware/photon/wiki/Downloading-Photon-OS">Downloading Photon OS</a> .<p></p><p><b>Minimal ISO</b>: ISO with generic or VMware hypervisor optimized installation</p><p><b>Full ISO </b>: The x86_64 ISO contains</p><p>- Photon Minimal</p><p>- Photon Developer</p><p>- Photon OSTree Host</p><p>- Photon Real Time</p><p>Photon Minimal and Photon Developer allow a generic or VMware hypervisor optimized installation. Photon OSTree Host allows a Default or Custom RPM-OSTree Server installation.</p><p><p></p><b>ISO Real-Time flavour</b>:  <a href="https://wiki.linuxfoundation.org/realtime/start">Linux Real-Time</a> optimized installation type</p><p></p><b>OVA</b>: VMware virtual machine hardware version dependent installation type, Secure Boot option</p></td>
	</tr>
	</tbody>
	</table>


1. Decide whether to use the OVA or ISO distribution to set up Photon OS.

    - **OVA import** : Because of the nature of an OVA, you're getting a pre-installed version of Photon OS. The OVA benefits from a simple import process and some kernel tuning for VMware environments. However, because it's a pre-installed version, the set of packages that are installed are predetermined.
    - **ISO install** : The ISO, on the other hand, allows for a more complete installation or automated installation via kickstart.

    To get Photon OS up and running quickly, use the OVA with VMware virtual machine hardware version 11 or higher.
    
    Depending on the Photon OS release, take [KB88737](https://kb.vmware.com/s/article/88737) into consideration for x86_64 Secure Boot.
    
    All distribution files support additional packages to be installed using tdnf.
    
1. Download Photon OS. Go to the following URL and download the latest release of Photon OS: <a href="https://github.com/vmware/photon/wiki/Downloading-Photon-OS">Downloading Photon OS</a>
    
    **Note:** For ISO installation, upload the ISO file to a datastore that is attached to the ESXi host, or mount the file share where the ISO resides as a datastore.
    Attach the ISO file to a virtual machine with VMware Photon OS 64-bit specified as guest os. Configure the virtual machine to boot from the ISO file.
    
