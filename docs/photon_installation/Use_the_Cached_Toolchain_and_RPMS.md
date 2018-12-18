# Use the Cached Toolchain and RPMS

When the necessary RPMs are available under `stage/RPMS/` directory, the commands that you use to create any Photon artifact such as, ISO or OVA will re use those RPMs to create the specified image.

If you already have the Photon RPMs available elsewhere, and not under `stage/RPMS/` in the Photon repository, you can build Photon artifacts using those cached RPMs by setting the PHOTON_CACHE_PATH variable to point to the directory containing those RPMs. 

For example, if your RPMs are located under `$HOME/photon-cache/`, then use the following command to build an ISO:
 
`sudo make iso PHOTON_CACHE_PATH=$HOME/photon-cache`

To use the cached toolchain, run the following command:

```
mkdir $HOME/photon-cache
sudo make iso PHOTON_CACHE_PATH=$HOME/photon-cache
```

The directory format of `$HOME/photon-cache/` is as follows:

```
photon-cache/:
                RPMS/:
                    noarch/*.rpm
                    x86-64/*.rpm
                    aarch64/*.rpm

```

**Note**: The `$HOME/photon-cache/` directory should follow the same structure as the `stage/RPMS/` directory.

