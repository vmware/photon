#!/bin/bash

#################################################
#	Title:	photon-build-machine-init        			#
# Date:	2015-03-17                        			#
# Version:	1.0				                          #
# Author:	tmcphail@vmware.com     	            #
# Options:					                            #
#################################################

PHOTON_WORKING=/workspaces/photon
PHOTON_HOST=/workspaces/host_srcroot

# Move to the workspace and cleanup any old build artifacts
cd ${PHOTON_WORKING}
sudo make clean

# Build toolchain
sudo make toolchain

# Build ISO
sudo make iso

# Remove the old stage directory on the host and copy the newly built one
if [[ -d ${PHOTON_HOST}/stage ]] ; then
  echo "Refreshing the host stage directory content..."
  rm -rf ${PHOTON_HOST}/stage
  cp -R ${PHOTON_WORKING}/stage ${PHOTON_HOST}/stage
else
  echo "Copying content to host stage directory..."
  cp -R ${PHOTON_WORKING}/stage ${PHOTON_HOST}/stage
fi

# Cleanup and shutdown (Halting the machine forces an rsync next time vagrant up)
echo "Cleanup the build..."
sudo make clean
echo "Shutting down the photon build machine..."
sudo shutdown -h now
