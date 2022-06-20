# kernel-fips-canister-builder

This project contains the source code of Photon FIPS canister implementation and the patches required in Photon kernel.

`crypto` folder contains source files that are newly added for canister implementation.

`patches` folder contains the additional kernel patches required for canister.
    
- 0001-FIPS-canister-binary-usage.patch - This patch can be used at two stages: Prerequisite patch for canister creation, Binary canister usage time.
- 0002-FIPS-canister-creation-secure.patch - This patch is required for creating canister from secure kernel.
- 0002-FIPS-canister-creation.patch - This patch is used for canister creation in all linux flavours.

To build the canister from secure kernel we need to use both the canister creation patches.

`build_fips_canister.sh` script helps in creating the canister binaries. 
`build_fips_canister.sh` script spawns a photon docker and builds linux RPM with canister source files and patches in docker.
This script takes linux flavor as an argument. [E.g: linux / linux-secure].

Workflow of this script is as follows:
    
1. Clones photon workspace in the current directory.
2. Copies linux specs and patches from photon workspace (`photon/SPECS/linux` folder) to `build/linux` folder.
3. Creates a patch file (canister-src-$CANISTER_SOURCE_VERSION.patch) from the canister source files present in crypto folder.
4. Modifies the linux spec (particular flavor spec file with the argument passed) and adds the 4 patches.
    0001-FIPS-canister-binary-usage.patch, 0002-FIPS-canister-creation-secure.patch, 0002-FIPS-canister-creation.patch, canister-src-$CANISTER_SOURCE_VERSION.patch
5. Unset %fips flag in linux spec file (This flag is only used when canister binary is consumed)
6. Spawns a docker 
7. Copies all the files from `build/linux` folder to /usr/src/photon/ folder and runs rpmbuild command
    

Once the build is completed the canister tarball is avaialble in `build/stage/canister-binaries` folder.

Canister tarball is versioned as `<CANISTER_SOURCE_VERSION-KERNEL_VERSION-FLAVOR>`

- `CANISTER_SOURCE_VERSION` - Canister source code version (currently 4.0.1)
- `KERNEL_VERSION` - This is taken from linux spec file (version-release) on which the canister is built.
- `FLAVOR` - Photon Linux Flavors (secure)
    
Logs are stored in `build/stage/LOGS` folder.

