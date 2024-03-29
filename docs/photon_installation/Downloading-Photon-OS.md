# Downloading Photon OS

You download Photon OS from https://github.com/vmware/photon/wiki/Downloading-Photon-OS.

Photon OS is available in the following pre-packaged, binary formats.

## Download Formats ####

<table style="height: 170px;" border="1" cellspacing="0" cellpadding="10">
<tbody>
<tr>
<td> Format </td><td> Description </td>
</tr>
<tr>
<td> ISO Image </td>
<td> Contains everything needed to install either the minimal or full installation of Photon OS. The bootable ISO has a manual installer or can be used with PXE/kickstart environments for automated installations. </td>
</tr>
<tr>
<td> OVA </td>
<td> Pre-installed minimal environment, customized for VMware hypervisor environments. These customizations include a highly sanitized and optimized kernel to give improved boot and runtime performance for containers and Linux applications. Since an OVA is a complete virtual machine definition, we've made available a Photon OS OVA that has virtual hardware version 11; this will allow for compatibility with several versions of VMware platforms or allow for the latest and greatest virtual hardware enhancements. </td>
</tr>
<tr>
<td> Amazon AMI </td>
<td> Pre-packaged and tested version of Photon OS made ready to deploy in your Amazon EC2 cloud environment. Previously, we'd published documentation on how to create an Amazon compatible instance, but, now we've done the work for you. </td>
</tr>
<tr>
<td> Google GCE Image </td><td> Pre-packaged and tested Google GCE image that is ready to deploy in your Google Compute Engine Environment, with all modifications and package requirements for running Photon OS in GCE. </td>
</tr>
<tr>
<td> Azure VHD </td>
<td> Pre-packaged and tested Azure HD image that is ready to deploy in your Microsoft Azure Cloud, with all modifications and package requirements for running Photon OS in Azure. </td>
</tr>
</tbody>
</table>


For cloud-ready images of Photon OS, see [Compatible Cloud Images](cloud-images.md).