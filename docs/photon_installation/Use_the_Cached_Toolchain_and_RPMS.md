# Use the Cached Toolchain and RPMS

When the necessary RPMs are available under the `stage/RPMS/` directory, the commands that you use to create any Photon artifact such as, ISO or OVA will reuse those RPMs to create the specified image.

If you already have the Photon RPMs available elsewhere, and not under `stage/RPMS/` in the Photon repository, you can build Photon artifacts using those cached RPMs by setting the `PHOTON_CACHE_PATH` variable to point to the directory containing those RPMs. 

For example, if your RPMs are located under `$HOME/photon-cache/`, then use the following command to build an ISO:
 
`sudo make iso PHOTON_CACHE_PATH=$HOME/photon-cache`

The `$HOME/photon-cache/` directory should follow the same structure as the `stage/RPMS/` directory:

```
photon-cache/:
├──RPMS/:
    ├──noarch/*.noarch.rpm
    ├──x86_64/*.x86_64.rpm
    ├──aarch64/*.aarch64.rpm

```


