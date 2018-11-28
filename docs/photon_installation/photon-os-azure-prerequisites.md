# Prerequisites

Before you use Photon OS with Microsoft Azure, perform the following prerequisite tasks:

1. Verify that you have a Microsoft Azure account. To create an account, see [https://azure.microsoft.com](https://azure.microsoft.com)

1. Install the latest version of Azure CLI. See [Install Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) and [Get started with Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest).

1. Verify that that you have a pair of SSH public and private keys. 

1. Download and extract the Photon OS VHD file.
    
    VMware packages Photon OS as a cloud-ready virtual hard disk (VHD file) that you can download for free from  [Bintray](https://bintray.com/vmware/photon). This VHD file is a virtual appliance with the information and packages that Azure needs to launch an instance of Photon in the cloud. After you have downloaded the distribution archive, extract the VHD file from it. You will later need to upload this VHD file to Azure, where it will be stored in an Azure storage account. For more information, see [Downloading Photon OS](Downloading-Photon-OS.md).