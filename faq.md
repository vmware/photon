#FAQ

#### Why can't I SSH in as root?

By default Photon does not permit root login to ssh. To make yourself login as root using
SSH set <code>PermitRootLogin yes</code> in /etc/ssh/sshd_config, and restart the sshd deamon.

#### Why netstat is not working?

netstat is deprecated, ss or ip (part of iproute2) should be used instead.

#### How to install new packages?
#### Why yum command is not working in minimal?

To install packages from cdrom, mount cdrom using following command

```
mount /dev/cdrom /media/cdrom
```

Then you can use __tdnf__ to install new pacakges

```
tdnf install vim
```

#### How to build new package RPM?

Assuming you have a ubuntu development environement setup and got the latest code pull into /workspace.
Lets assume your package name is foo with version 1.0.

```
cp foo-1.0.tar.gz /workspace/photon/SOURCES
cp foo.spec /workspace/photon/SPECS/foo/
cd /workspace/photon/support/package-builder
sudo python ./build_package.py -i foo
```

#### I just booted into freshly installed Photon, why <code> docker ps </code> not working?

Make sure docker daemon is running, which by design is not started at boot time. 

#### What is the difference between Micro/Minimal/Full installation of Photon?
Micro is smallest version under 220MB (as of 03/30) to be used as base for customization.

Minimal is Micro plus Docker and Cloud-init packages.

Full contains all the packages shipped with ISO.

#### What packages are included in Micro/Minimal?
See [package_list.json](installer/package_list.json)

#### Why vi/vim is not working in Minimal Photon?

We have `nano` installed by default for file editing in Minimal. Use `tdnf` to install `vim`.

#### How to transfer/share files between Photon and my host machine?

We are working on supporting some standard options. Currently I am using [sshfs](https://wiki.archlinux.org/index.php/sshfs) for file sharing between host and Photon.
