This guide describes how to get started using Photon OS as a virtual machine within VMware Workstation. It provides instructions for downloading Photon OS (as an OVA or ISO file), describes the various installation options, and walks through the steps of installing the Photon OS distribution on Workstation. Once Photon OS is installed, this document shows how to deploy a containerized application in Docker with a single command.

- [About Photon OS](#about-photon-os)
- [Requirements](#requirements)
- [Deciding Whether to Use OVA or ISO](#deciding-whether-to-use-ova-or-iso)
- [Downloading Photon OS](#downloading-photon-os)
- [Importing the OVA for Photon OS 2.0](#importing-the-ova-for-photon-os-20)
- [Installing the ISO Image for Photon OS 2.0](#installing-the-iso-image-for-photon-os-20)
- [Deploying a Containerized Application in Photon OS](#deploying-a-containerized-application-in-photon-os)
- [Installing Photon OS 1.0](#installing-photon-os-10)

**Note**: If you want to upgrade an existing Photon 1.0 VM, refer to the instructions in [Upgrading to Photon OS 2.0](https://github.com/vmware/photon/wiki/Upgrading-to-Photon-OS-2.0). 

# About Photon OS

Photon OS™ is an open source Linux container host optimized for cloud-native applications, cloud platforms, and VMware infrastructure. Photon OS provides a secure run-time environment for efficiently running containers. For an overview, see  [https://vmware.github.io/photon/](https://vmware.github.io/photon/).

# Requirements

Using Photon OS within VMware Workstation requires the following resources:

| **Resource** | **Description** |
| --- | --- |
| VMware Workstation | VMware Workstation must be installed (Workstation 10 or higher). The latest version is recommended. |
| Memory | 2GB of free RAM (recommended) |
| Storage | **Minimal Photon install** : 512MB of free space (minimum); **Full Photon install** : 4GB of free space (minimum); 8GB is recommended |
| Distribution File | Photon OS ISO or OVA file downloaded from bintray ([https://bintray.com/vmware/photon/](https://bintray.com/vmware/photon/)).

Resource requirements and recommendations vary depending on several factors, including the host environment (for example, VMware Workstation and VMware vSphere), the distribution file used (ISO or OVA), and the selected installation settings (for example, full or basic installation).

**Note:**  The setup instructions in this guide use VMware Workstation Professional version 12.5.7.

[[/images/ws_version.png]]

# Deciding Whether to Use OVA or ISO

The first step is decide whether to use the the OVA or ISO distribution to set up Photon OS.

- **OVA import** : Because of the nature of an OVA, you&#39;re getting a pre-installed version of Photon OS. For Workstation, choose the OVA with Hardware Version 11 (_not_ 13). The OVA benefits from a simple import process and some kernel tuning for VMware environments. However, because it&#39;s a pre-installed version, the set of packages that are installed are predetermined. Any additional packages that you need can be installed using tdnf.
- **ISO install** : The ISO, on the other hand, allows for a more complete installation or automated installation via kickstart.

If you&#39;re just looking for the fastest way to get up and running, start with the OVA.

# Downloading Photon OS

Once you&#39;ve decided which way to install, you&#39;ll need to download the correct binaries. Go to the following Bintray URL and download the latest release of Photon OS:

[https://bintray.com/vmware/photon/](https://bintray.com/vmware/photon/)

For instructions, see  [Downloading Photon OS](https://github.com/vmware/photon/wiki/Downloading-Photon-OS).

# Importing the OVA for Photon OS 2.0

Using the OVA is the easiest way to create a Photon OS VM on VMware Workstation.

## Step 1: Start the Import Process

After you&#39;ve downloaded the OVA file (OVA with Hardware Version 11), do one of the following:

- Double-click it to start the import process, or
- Start VMware Workstation and, from the File menu, choose **Open**.

[[/images/ws-ova-import.png]]

## Step 2: Specify the Name and Storage Location

Change the name and storage location, if you want.

[[/images/ws-ova-path.png]]

Choose **Import**.

[[/images/ws-ova-license.png]]

Review the License Agreement and choose **Accept**.

## Step 3: Configure VM Settings

Once the OVA is imported, Workstation displays a summary of the settings for your Photon OS VM.

[[/images/ws-ova-settings.png]]

Choose **Edit virtual machine settings**. Workstation displays the Virtual Machine settings. You can either accept the defaults or change settings as needed.

[[/images/ws-ova-settings-edit.png]]

Select the Options tab.

[[/images/ws-ova-settings-options.png]]

Under Guest operating system, select **Linux**.

For Version, click the list and select **VMWare Photon 64-bit**.

[[/images/ws-ova-os.png]]

**Note:**  If you want to configure a secure boot for the Photon OS VM, select **Advanced**  and select (check) **Boot with EFI instead of BIOS**. The EFI boot ensures that the ISO content is signed by VMware and that the entire stack is secure.

[[/images/ws-ova-settings-efi.png]]

Choose **OK**.

## Step 4: Power on the VM

From the tab, choose  **Power on this virtual machine**.

[[/images/ws-ova-splash.png]]

After the splash screen, Workstation will prompt you to log in.

## Step 5: Update Login Credentials

**Note** : Because of limitations within OVA support on Workstation, it was necessary to specify a default password for the OVA option. However, all Photon OS instances that are created by importing the OVA will require an immediate password change upon login. The default account credentials are:

| **Setting** | **Value** |
| --- | --- |
| Username | ``root`` |
| Password | ``changeme`` |

After you provide these credentials, Workstation prompts you to create a new password and type it a second time to verify it. For security, Photon OS forbids common dictionary words for the root password. Once logged in, you will see the shell prompt.

[[/images/ws-ova-password.png]]

Once complete, proceed to [Deploying a Containerized Application in Photon OS](#deploying-a-containerized-application-in-photon-os).

# Installing the ISO Image for Photon OS 2.0

After you have downloaded the Photon OS ISO image into a folder of your choice, open VMware Workstation.

## Step 1: Start the Installation Process

From the File menu, choose **New Virtual Machine**  to create a new virtual machine.

[[/images/ws-iso-new.png]]

Select **Typical** or **Custom**, and then choose **Next**. These instructions refer to a Typical installation.

[[/images/ws-iso-typical.png]]

## Step 2: Select the ISO Image

Select **Installer disc image file (iso)**, choose **Browse** and select the Photon OS ISO file.

[[/images/ws-iso-selected.png]]

## Step 3: Select the Operating System

Choose **Next**. Select the Guest operating system.

For the Guest operating system, select **Linux**.

Click the Version dropdown and select **VMware Photon 64-bit**  from the list.

[[/images/ws-iso-os.png]]

## Step 4: Specify the VM Name and Location

Choose **Next**. Specify a virtual machine name and location.

[[/images/ws-iso-name.png]]

## Step 5: Specify Disk Options

Choose **Next**. Specify the maximum disk size and whether you want to split the virtual disk into multiple files or store it as a single file.

[[/images/ws-iso-disk.png]]

## Step 6: Configure VM Settings

Choose **Next**. Workstation displays a summary of your selections.

[[/images/ws-iso-summary.png]]

**Important** : _Before_ you finish creating the Photon OS Virtual Machine, we strongly recommend that you customize the virtual machine and remove any unwanted devices that are not needed for a container run-time environment. To remove unnecessary devices, choose **Customize hardware**.

[[/images/ws-iso-customize.png]]

Consider removing the following components, which are not used by Photon OS:

- Select **Sound Card**, un-tick the **Connect at power on** option. Confirm your action and choose **Close** to return to the VM Settings by .
- Select **USB Controller** and ensure that the **Share Bluetooth devices with the virtual machine** setting is unchecked (it should be unchecked, by default) and then choose **Close**.
- Select **Display** and ensure that the **Accelerate 3D Graphics** option is unchecked (it should be unchecked, by default) and then choose **Close**.
- At this stage we have now made all the necessary customizations and you are ready to select the Photon OS ISO image to boot and begin the installation process.
- Choose  **Finish**.

In Workstation, choose **Edit virtual machine settings**, select **CD/DVD (IDE)**, and verify that **Connect at power on** is selected.

[[/images/ws-iso-cd.png]]

## Step 7: Configure a Secure Boot (Optional)

**Note:**  If you want to configure a secure boot for the Photon OS VM, in Workstation, choose  **Edit virtual machine settings**, select  **Options**, choose **Advanced**, and select **Boot with EFI instead of BIOS**.

[[/images/ws-iso-efi.png]]

The EFI boot ensures that the ISO content is signed by VMware and that the entire stack is secure.

Choose **OK**.

[[/images/ws-iso-settings.png]]

## Step 8: Power On the VM

Choose **Power on this virtual machine**.

When you see the Photon Installer boot menu, press Enter on your keyboard to start installing.

[[/images/ws-iso-installer.png]]

Review the license agreement.

[[/images/ws-iso-license.png]]

Choose **Accept** and press Enter.

## Step 9: Configure the Partition

The installer will detect one disk, which should be the 8GB volume configured as part of the virtual machine creation. Choose **Auto**  to have the installer automatically allocate the partition, or choose **Custom**  if you want to configure individual partitions, and then press the Enter key.

[[/images/ws-iso-disk-partition.png]]

**Note:**  If you choose Custom, the installer displays the following screen.

[[/images/ws-iso-disk-partition-custom.png]]

For each custom partition, choose **Create New**  and specify the following information:

[[/images/ws-iso-disk-partition-new.png]]

**Size** - Preallocated size of this partition, in MB.

**Type** - One of the following options:

- **ext3** - ext3 file system
- **ext4** - ext4 file system
- **swap** - swap partition

**Mountpoint** - Mount point for this partition.

Choose **OK** and press the Enter key. When you are done defining custom partitions, choose **Next** and press the Enter key.

The installer prompts you to confirm that you want to erase the entire disk. Choose  **Yes**  and press the Enter key.

[[/images/ws-iso-disk-erase.png]]

## Step 10: Select an Installation Option

After partitioning the disk, the installer will prompt you to select an installation option.

[[/images/ws-iso-install-option.png]]

Each installation option provides a different run-time environment, depending on your requirements.

| **Option** | **Description** |
| --- | --- |
| **Photon Minimal** | Photon Minimum is a very lightweight version of the container host runtime that is best suited for container management and hosting. There is sufficient packaging and functionality to allow most common operations around modifying existing containers, as well as being a highly performant and full-featured runtime. |
| **Photon Full** | Photon Full includes several additional packages to enhance the authoring and packaging of containerized applications and/or system customization. For simply running containers, Photon Full will be overkill. Use Photon Full for developing and packaging the application that will be run as a container, as well as authoring the container, itself. For testing and validation purposes, Photon Full will include all components necessary to run containers. |
| **Photon OSTree Server** | This installation profile will create the server instance that will host the filesystem tree and managed definitions for rpm-ostree managed hosts created with the &quot;Photon OSTree Host&quot; installation profile. Most environments should need only one Photon OSTree Server instance to manage the state of the Photon OSTree Hosts. Use Photon OSTree Server when you are establishing a new repository and management node for Photon OS hosts. |

**Note:**  The option you choose determines the disk and memory resources required for your installation.

Select the option you want and press the Enter key.

## Step 11: Select the Linux Kernel

Select a Linux kernel to install.

[[/images/ws-iso-kernel.png]]

- **Hypervisor optimized** means that any components that are not needed for running under a VMware hypervisor have been removed for faster boot times.
- **Generic** means that all components are included.

Choose **Next** and press the Enter key.

## Step 12: Specify the Hostname

The installer prompts you for a hostname and suggest a randomly generated, unique hostname that you can change if you want.

[[/images/ws-iso-hostname.png]]

Press the Enter key.

## Step 13: Specify the System root Password

**_Note_** _: Photon OS will not permit commonly used dictionary words to be set as a root password._

The installer prompts you to enter the system root password. Type the password and press the Enter key.

[[/images/ws-iso-root-password.png]]

The installer prompts you to confirm the root password by typing it a second time.

[[/images/ws-iso-root-password-confirm.png]]

Press the Enter key. The installer proceeds to install the software. Installation times will vary based on the system hardware and installation options you selected. Most installations complete in less than one minute.

## Step 14: Reboot the VM and Log In

Once finished, the installer displays a confirmation message (which includes how long it took to install Photon OS) and prompts you to press a key on your keyboard to boot the new VM.

[[/images/ws-iso-installed.png]]

Press any key on the keyboard and the virtual machine will reboot into Photon OS.

As the initial boot process begins, the installer displays the Photon splash screen, and then a login prompt.

[[/images/ws-iso-splash.png]]

At the login prompt, type **root**  as the username and provide the password chosen during the installation.

[[/images/ws-iso-login.png]]

You have now successfully set up Photon OS and are ready to use your container run-time environment. Proceed to the next section to deploy a containerized application.

# Deploying a Containerized Application in Photon OS

Now that you have your container runtime environment up and running, you can easily deploy a containerized application. For this example, you will deploy the popular open source Web Server Nginx. The Nginx application has a customized VMware package that is published as a dockerfile and can be downloaded directly through the Docker module from the Docker Hub.

## Step 1: Run Docker

To run Docker from the command prompt, enter the following command, which initializes the docker engine:

    systemctl start docker

To ensure Docker daemon service runs on every subsequent VM reboot, enter the following command:

    systemctl enable docker

## Step 2: Run the Nginx Web Server

Now the Docker daemon service is running, it is a simple task to &quot;pull&quot; and start the Nginx Web Server container from Docker Hub. To do this, type the following command:

    docker run -d -p 80:80 vmwarecna/nginx

This pulls the Nginx Web Server files and appropriate dependent container filesystem layers required for this containerized application to run.

[[/images/ws-docker-run.png]]

After the **docker run**  process completes, you return to the command prompt. You now have a fully active website up and running in a container.

## Step 3: Test the Web Server

To test that your Web Server is active, run the **ifconfig** command to get the IP address of the Photon OS Virtual Machine.

[[/images/ws-docker-ifconfig.png]]

The output displays a list of adapters that are connected to the virtual machine. Typically, the web server daemon will be bound on &quot; **eth0**&quot;.

Start a browser on your host machine and enter the IP address of your Photon OS Virtual Machine (the **inet addr** for eth0). You should see a screen similar to the following example as confirmation that your web server is active.

[[/images/ws-docker-confirm.png]]

You can now run any other containerized application from Docker Hub or your own containerized application within Photon OS.

# Installing Photon OS 1.0

Refer to the Photon OS 1.0 installation instructions in [Running Photon OS on Fusion](https://github.com/vmware/photon/wiki/Running-Project-Photon-on-Fusion).