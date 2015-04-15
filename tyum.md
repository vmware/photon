#default package manager in photon - tdnf(tyum)

##Introduction
tdnf(tyum) is tiny dnf (tiny yum) implementing dnf commands in C without python dependencies. 
dnf is the next upcoming major version of yum. tyum(tdnf) is included in photon micro, photon minimal and photon full. 
tyum(tdnf) will read yum repositories and work just like yum. If you need yum, its just as easy as ```tdnf install yum```

##How to configure a repository
photon comes pre-configured with ```photon-iso``` repository which is in ```\etc\yum.repos.d```
If you get an access error message when working with this repository, it is usually because you dont have the
photon iso mounted. If you have the photon iso, you can mount and makecache to read metadata.

```
mount /dev/cdrom /media/cdrom
tdnf makecache
```

##How to install a package?
```tdnf install pkgname```

##How to remove a package
```tdnf erase pkgname```

##How to list enabled repositories
```tdnf repolist```

##Other commands
tdnf implements all dnf commands as listed here: http://dnf.readthedocs.org/en/latest/
