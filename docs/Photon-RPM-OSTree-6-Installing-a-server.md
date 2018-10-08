This is the server that is going to be used by a system administrator or a package installer developer to compose filesystem trees and make them available to hosts (or clients) to pull (download) and deploy.  

The first step is to download the ISO for the desired release, if you have not done that already:  
[[Photon 1.0 GA ISO file|https://bintray.com/artifact/download/vmware/photon/photon-1.0-13c08b6.iso]]  
[[Photon 1.0 Rev2 ISO file|https://bintray.com/artifact/download/vmware/photon/photon-1.0-62c543d.iso]]  
[[Photon OS 2.0 Beta ISO file|https://bintray.com/vmware/photon/download_file?file_path=2.0%2FBeta%2Fiso%2Fphoton-2.0-8553d58.iso]]  

Installation steps are the same to all Photon OS versions, except that under the hood:
* Photon 1.0 sets up a 'minimal' sample file tree, so it's ready to accept host pull/install requests right away.
* Photon 2.0 does not set up a file tree, so there are several steps needed post-install to have a completely functional server that host can deploy from; they will be explained in detail in Chapter 8 and 9, but a quick setup is provided for you later in this chapter.  

### 6.1 Manual install of a server
First, create a new VM in Fusion, Workstation or ESXi box, and go through the [[steps common to all installation profiles|Running-Project-Photon-on-Fusion]], then select the "Photon OSTree Server" option.

![PhotonChooseServer](https://cloud.githubusercontent.com/assets/13158414/14802949/1c5f92b8-0b0a-11e6-8d69-96e62218dfcb.png)

Continue with setting up a host name (like photon-srv) and a root password and that's all you need. Installation took about 40 seconds for Fusion running on my Mac with SSD, but it should take longer time for spin hard drives.  

For Photon 1.0, once the server boots, the RPM-OSTree repository is ready to accept pull request from hosts, because setting up a 'minimal' tree is part of installation. This ostree 'minimal' configuration is almost identical, as far as packages list, to the 'Photon Minimal' installation profile from 'Select Installation' menu. 

![PhotonServerLogin](https://cloud.githubusercontent.com/assets/13158414/14802957/2f5ed7e8-0b0a-11e6-960d-04c6202b0c4e.png)


In order for hosts to access server's OSTree repo via http, an Apache web server is configured as part of installation. If you want to also serve https, you need to take additional steps - configure the web server, open port 443 via iptables and install certificates specific to your organization, that I won't cover here.  

The server's IP address will be passed to the Photon RPM-OSTree hosts that want to connect to this server.  
You may ask your network administrator for a static IP, registered to your company's DNS, so your users who install Photon RPM-OSTree hosts will enter a pretty name like http://photon-srv.yourcompany.com, rather than remember a numeric IP address.

Having the server configured, you may advance to next chapter to [[install your own host from this server's repository|Photon-RPM-OSTree:-7-Installing-a-host-against-a-custom-server-repository]]. That's a way to verify right away that all components (server, network) are running correctly and test the 'minimal' server filetree image by downloading and installing it at the host.

### 6.2 Composing your first OSTree repo  
If you've installed Photon 2.0 OSTree server, the server did not setup a tree as part of an installation, but configuration files for starter 'base', 'minimal' and 'full' tree are there for you. To create a 'minimal' tree, you only need two commands - one to initialize a new repo, the other one to compose it.
```
root [ ~ ]# cd /srv/rpm-ostree
root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
```
You are now ready to deploy a host, explained in next chapter. Skip to [[Chapter 8: File oriented server operations|Photon-RPM-OStree:-8-File-oriented-server-operations]] and [[Chapter 9: Package oriented server operations|Photon-RPM-OSTree:-9-Package-oriented-server-operations]] to learn create your own customized file tree.   

### 6.2 Automated install of a server via kickstart
All Photon OS versions support unattended install, in other words installer will display its progress, but will not prompt for any keys to be clicked, and will boot at the end of installation. This will create an identical server as installing via UI.

If not familiar with the way kickstart works, visit [[Kickstart Support in Photon OS|https://github.com/vmware/photon/blob/master/docs/kickstart.md]]. The kickstart json config for OSTree is similar to minimal or full, except for this setting:  
```
"type": "ostree_server"
```

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-5-Host-updating-operations]] | [[Next page >|Photon-RPM-OSTree:-7-Installing-a-host-against-a-custom-server-repository]]