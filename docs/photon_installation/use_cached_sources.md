# Use Cached Sources

To use the cached sources, run the following command:

```
mkdir $HOME/photon-sources
sudo make iso PHOTON_SOURCES_PATH=$HOME/photon-sources
```
The directory format of `PHOTON_SOURCES_PATH` is as follows:

```
photon-sources/
├──src1.tar.gz
├──src2.tar.gz
└──...
```
