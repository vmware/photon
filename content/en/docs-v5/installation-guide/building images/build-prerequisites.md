---
title: Build Prerequisites
weight: 2
---

Before you build the ISO, verify that you have performed the following tasks:

* Installed a build operating system running the 64-bit version of Ubuntu 14.04 or later version.

  Downloaded and installed the following packages for Ubuntu:  
  
  More than one line beginning with `apt-get -y install` is shown for better legibility.  
  ```console
  apt-get -y install bc bison createrepo g++ gawk genisoimage git
  apt-get -y install kpartx libfuse-dev libreadline-dev libssl-dev        
  apt-get -y install python-aptdaemon python-requests texinfo uuid-dev
  ```
        
* Installed a build operating system running Photon OS 3.0 or later version.

  Downloaded and installed the following packages for Photon OS:  
  
  More than one line beginning with `tdnf install -y` is shown for better legibility.
  ```console
  tdnf install -y bc build-essential cdrkit createrepo_c
  tdnf install -y dosfstools docker docker-py3 git kpartx openssl-devel
  tdnf install -y python3-curses python3-pip python3-pyOpenSSL python3-six
  tdnf install -y rsync rpm-build util-linux-devel zlib-devel
  ```

* Verify that the Docker Engine is up and running. For example, run

  ```console
  docker run -it hello-world
  ```

* Downloaded source code from the Photon OS repository on GitHub into `$HOME/workspaces/photon`. For example, run

  ```console
  mkdir -p $HOME/workspaces
  cd $HOME/workspaces
  git clone -b 5.0 https://www.github.com/vmware/photon.git
  ```
