#!/bin/bash

. /etc/lsb-release

echo "==> OS detected: ${DISTRIB_ID} ${DISTRIB_RELEASE} (${DISTRIB_CODENAME})"
echo "==> Setting up puppet from apt.puppetlabs.com"
wget https://apt.puppetlabs.com/puppetlabs-release-${DISTRIB_CODENAME}.deb
dpkg -i puppetlabs-release-${DISTRIB_CODENAME}.deb
rm puppetlabs-release-${DISTRIB_CODENAME}.deb
apt-get update
apt-get install -y puppet
