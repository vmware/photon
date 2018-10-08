Organizations that maintain their own OSTree servers create custom image trees suited to their needs from which hosts can be deployed and upgraded. One single server may make available several branches to install, for example "base", "minimal" and "full". Or, if you think in terms of Windows OS SKUs - "Home", "Professional" or "Enterprise" edition.

So in fact there are two pieces of information the OSTree host installer needs - the server URL and the branch ref. Also, there are two ways to pass this info - manually via keyboard, when prompted and automated, by reading from a config file.

### 7.1 Manual install of a custom host
For Photon 1.0 or 1.0 Revision 2, installing a Photon RPM-OSTree host that will pull from a server repository of your choice is very similar to the way we installed the host against the default server repo in [[Chapter 2|Photon-RPM-OSTree:-2-Installing-a-host-against-default-server-repository]].  
We will follow the same steps, selecting "Photon OSTree Host", and after assigning a host name like **photon-host** and a root password, this time we will click on "Custom RPM-OSTree Server".  

![PhotonHostCustom](https://cloud.githubusercontent.com/assets/13158414/14804629/fe17c7d4-0b19-11e6-9cc6-7e79f768b7b1.png)

An additional screen will ask for the URL of server repo - just enter the IP address or fully qualified domain name of the [[server installed in the previous step|Photon-RPM-OSTree:-6-Installing-a-server]].  

![PhotonHostCustomURL](https://cloud.githubusercontent.com/assets/13158414/14804647/185f1aa2-0b1a-11e6-9e44-e2f54592da35.png)

You will then be asked to enter a Refspec. Leave the default 'photon/1.0/x86_64/minimal' value, unless you've created a new branch at the server (we will see later how to do that).  

![PhotonHostCustomRefspec](https://cloud.githubusercontent.com/assets/13158414/14804653/1f0d31cc-0b1a-11e6-8f56-e8cac1f72852.png)

Once this is done and the installation finished, reboot and you are ready to use it.  
You may verify - just like in [[Chapter 3.1|Photon-RPM-OStree:-3-Concepts-in-action#31-querying-the-deployed-filetrees]] - that you can get an rpm-ostree status. The value for the CommitID should be identical to the [[host that installed from default repo|Photon-RPM-OSTree:-2-Installing-a-host-against-default-server-repository]], if the [[server|Photon-RPM-OSTree:-6-Installing-a-server]] has been installed fresh, from the same ISO.  

Photon 2.0 does not provide the UI option to install an RPM-OSTree host, but supports automated, UI-less install, that we'll explore next.

### 7.2 Automated install of a custom host via kickstart
Photon 1.0, 1.0 Revision 2 and Photon OS 2.0 support automated install that will not interact with the user, in other words installer will display its progress, but will not prompt for any keys to be clicked, and will boot at the end of installation.  

If not familiar with the way kickstart works, visit [[Kickstart Support in Photon OS|https://github.com/vmware/photon/blob/master/docs/kickstart.md]]. The kickstart json config for OSTree is similar to minimal or full, except for these settings that should sound familiar: 
```
    ...
    "type": "ostree_host",
    "ostree_repo_url": "http://192.168.218.249",
    "ostree_repo_ref": "photon/1.0/x86_64/minimal",
    ...
```
If the server is Photon OS 2.0, and the administrator composed trees for the included json files, the ostree_repo_ref will take either value: **photon/2.0/x86_64/base**, **photon/2.0/x86_64/minimal**, or **photon/2.0/x86_64/full**.

In most situations, kickstart file is accessed via http from PXE boot. That enables booting from network and end to end install of hosts from pre-defined server URL and branch without assistance from user. 

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous Page|Photon-RPM-OSTree:-6-Installing-a-server]] | [[Next page >|Photon-RPM-OStree:-8-File-oriented-server-operations]]