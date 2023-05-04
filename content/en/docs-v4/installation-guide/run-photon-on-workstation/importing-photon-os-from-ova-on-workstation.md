---
title:  Importing the OVA for Photon OS 4.0
weight: 2
---

Using the OVA is the easiest way to create a Photon OS VM on VMware Workstation. 

After you have downloaded the OVA file (for example, OVA UEFI with Hardware Version 13), perform the following steps:

1. Start the Import Process

    - Double-click it to start the import process, or
    - Start VMware Workstation and, from the File menu, choose **Open**.

1.  License

    ![License](../../images/ws17-ova-license.png)
    
    Review the License Agreement and choose **Accept**.

1. Specify the Name and Storage Location

    Change the name and storage location, if you want.
    
    ![Name and Storage Location](../../images/ws17-ova-uefi-vhw13-import.png)
    
    Choose **Import**.

1. Configure VM Settings

    Once the OVA is imported, Workstation displays a summary of the settings for your Photon OS VM.
    
    ![Settings](../../images/ws17-ova-uefi-vhw13-settings.png)
    
    Choose **Edit virtual machine settings**. Workstation displays the Virtual Machine settings. You can either accept the defaults or change settings as needed.
    
    ![OVA settings](../../images/ws17-ova-uefi-vhw13-settings-hardware.png)
    
    Select the Options tab.
    
    ![Options](../../images/ws17-ova-uefi-vhw13-settings-options.png)

    Under Guest operating system,  **Linux** is preselected.
    
    For Version, **VMWare Photon 64-bit** is preselected.
    
    For the UEFI OVA, **UEFI** as firmware type is preconfigured. UEFI ensures that the ISO/OVA content is signed by VMware and that the entire stack is secure.
    
    ![UEFI boot](../../images/ws17-ova-uefi-vhw13-settings-uefi.png)
    
    Choose **OK**.

1. Power on the VM

    From the tab, choose  **Power on this virtual machine**.
    
    ![OVA splash](../../images/Photon-4-bootsplash.png)
    
    After the splash screen, Workstation will prompt you to log in.

1. Update Login Credentials

    **Note** : Because of limitations within OVA support on Workstation, it was necessary to specify a default password for the OVA option. However, all Photon OS instances that are created by importing the OVA will require an immediate password change upon login. The default account credentials are:
    
    - Username: ``root``
    - Password: ``changeme``
    
    After you provide these credentials, Workstation prompts you to create a new password and type it a second time to verify it. For security, Photon OS forbids common dictionary words for the root password. Once logged in, you will see the shell prompt.
    
    ![OVA password](../../images/ws17-ova-uefi-vhw13-password.png)
    
    Once complete, proceed to [Deploying a Containerized Application in Photon OS](../deploying-a-containerized-application-in-photon-os/).
