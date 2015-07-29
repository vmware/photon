# What is OSTree and RPM-OSTree
OSTree is a tool for managing bootable, immutable, versioned filesystem trees.

## Photon RPM-OSTree Server
During installation from Photon ISO you can select "Photon RPM-OSTree Server" option that will install Photon with RPM-OSTree components and a minimal repo from which RPM-OSTree Hosts could be created.

On RPM-OSTree Server the repo is created at following location.
```
/srv/rpm-ostree/repo
```
Following is the base configuration file used to create the repo.
```
/srv/rpm-ostree/photon-base.json
```
### Updating RPM-OSTree repo image

You can add/remove package from photon-base.json file and then run following command to update the repo with new commit.
```
cd /srv/rpm-ostree
rpm-ostree compose tree --repo=/srv/rpm-ostree/repo photon-base.json
```

Above command will create a new commit that will have your package related changes in it.

### Changing the RPM repo
Following is the rpm repo file being used for fetching RPMs by the rpm-ostree command to create the ostree repo. Change this file to point to different rpm repo than the default Photon repo.

```
/srv/rpm-ostree/photon-ostree.json
```

## RPM-OSTree Host

OSTree host is the installation of Photon that retrives the images from RPM-OSTree server during installation. It can get atomic updates from the same server in its life time.

## Upgrading the Host installations

Host machines created from RPM-OSTree server can run following commands to upgrade their Host machine to the latest version from RPM-OSTree server.

```
> ostree pull photon tp2/x86_64/minimal
> rpm-ostree upgrade
> systemctl reboot
```
