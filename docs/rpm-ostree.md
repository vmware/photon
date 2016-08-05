# What is OSTree and RPM-OSTree?
OSTree is a tool for managing bootable, immutable, versioned filesystem trees.

## Photon RPM-OSTree Server
During installation from the Photon OS ISO, you can select the `Photon RPM-OSTree Server` option to install Photon OS with the RPM-OSTree components and a minimal repository from which RPM-OSTree Hosts can be created.

On RPM-OSTree Server the repo is created at the following location: 
```
/srv/rpm-ostree/repo
```
Here is the base configuration file that creates the repo:
```
/srv/rpm-ostree/photon-base.json
```
### Updating RPM-OSTree Repo Image

You can add or remove packages from the `photon-base.json` file and then run following commands to update the repo with a new commit:
```
cd /srv/rpm-ostree
rpm-ostree compose tree --repo=/srv/rpm-ostree/repo photon-base.json
```
The command above creates a new commit that contains your package-related changes.

## RPM-OSTree Host

OSTree host is an installation of Photon OS that retrieves the images from RPM-OSTree server during installation. It can get atomic updates from the same server during its lifecycle.

## Upgrading the Host Installations

Host machines created from RPM-OSTree server can run the following commands to upgrade their host machine to the latest version from the RPM-OSTree server:

	rpm-ostree upgrade
	systemctl reboot

