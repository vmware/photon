#!/bin/bash

git clone https://github.com/rasa/vmware-tools-patches.git
cd vmware-tools-patches
sudo ./download-tools.sh 8.0.2
sudo ./untar-and-patch.sh
cd vmware-tools-distrib
sudo ./vmware-install.pl -f -d --clobber-kernel-modules=pvscsi,vmblock,vmci,vmhgfs,vmmemctl,vmsync,vmxnet,vmxnet3,vsock
cd "$HOME"
rm -rf vmware-tools-patches
