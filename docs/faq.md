#FAQ

#### Why can't I SSH in as root?

By default Photon does not permit root login to ssh. To make yourself login as root using
SSH set <code>PermitRootLogin yes</code> in /etc/ssh/sshd_config, and restart the sshd deamon.

#### Why is netstat not working?

netstat is deprecated, ss or ip (part of iproute2) should be used instead.

This [Guide](https://dougvitale.wordpress.com/2011/12/21/deprecated-linux-networking-commands-and-their-replacements/) guide depicts the most common examples.

#### How do I install new packages?
#### Why is the yum command not working in a Minimal installation of Photon?

tdnf is default package manager to install new packages. Its a C implementation of DNF package manager. See [DNF documentation](https://media.readthedocs.org/pdf/dnf/latest/dnf.pdf) for detailed help on commands.

Examples:

To install new package

```
tdnf install vim
```

To check available upgrades

```
tdnf check-update
```

To upgrade package

```
tdnf upgrade vim
```

To refresh repository cache

```
tdnf makecache
```

#### How do I build a new RPM package?

Assuming you have the Ubuntu development environment setup and got the latest code pull into /workspace.
Lets assume your package name is foo with version 1.0.

```
cp foo-1.0.tar.gz /workspace/photon/SOURCES
cp foo.spec /workspace/photon/SPECS/foo/
cd /workspace/photon
sudo make foo
```

#### I just booted into a freshly installed Photon, why is ```docker ps``` not working?

Make sure the docker daemon is running, which by design is not started at boot time.

#### What is the difference between the Micro/Minimal/Full installations of Photon?
Micro is the smallest version of Photon, under 220MB (as of 03/30) to be used as base for customization.

Minimal is Micro plus Docker and Cloud-init packages.

Full contains all the packages shipped with ISO.

#### What packages are included in Minimal?
See [packages_minimal.json](../common/data/packages_minimal.json) for Minimal packages.

#### Why is vi/vim not working in a Minimal installation of Photon?

We have `nano` installed by default for file editing in Minimal. Use `tdnf` to install `vim`.

#### How do I transfer/share files between Photon and my host machine?

We are working on supporting some standard options. Currently we recommend using [sshfs](https://wiki.archlinux.org/index.php/sshfs) for file sharing between hosts and Photon.
