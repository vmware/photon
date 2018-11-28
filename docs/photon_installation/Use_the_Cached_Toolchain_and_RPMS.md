# Use the Cached Toolchain and RPMS

To use the cached toolchain, run the following command:

```
mkdir $HOME/photon-cache
sudo make iso PHOTON_CACHE_PATH=$HOME/photon-cache
```

The directory format of `PHOTON_CACHE_PATH` is as follows:

```
photon-cache/
├──tools-build.tar.gz
├──RPMS/x86-64/*.rpm
└──RPMX/noarch/*.rpm
```