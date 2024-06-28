Automated Photon OS Livepatching
Collection of scripts that can be used to automatically generate livepatches for Photon OS.
Must be run inside of a shell, i.e with bash.

****** auto_livepatch.sh ******
auto_livepatch runs gen_livepatch inside a docker container, which makes it easier to control the build environment, and can build livepatches for any Photon OS version/flavor.

auto_livepatch.sh [options] -p [list of patch files]

Options:

-k: Specifies the kernel version. If not set, uses uname -r
-p: Patch file list. Need at least one patch file listed here
-n: Output file name. Will be default if not specified.
-o: Output directory. Will be default if not specified.
-R: Disable replace flag (replace flag is on by default)
-d: Use file contents as description field for livepatch module.
-s: Specify the path to a local source rpm
-v: Specify the path to a local debuginfo rpm
--export-debuginfo: Saves debug files after module is built.
--rpm: Package the module inside of an rpm.
--rpm-version: Set the version number for the rpm.
--rpm-release: Set the release number for the rpm.
--rpm-desc: Set a separate description for the rpm. Input is a file.
-h/--help: Prints help message and exits

** Examples **

Simplest Usage - Build livepatch for current kernel

    auto_livepatch.sh -p example.patch


Set non-replace flag and save debug information

    auto_livepatch.sh -p example.patch -R --exportdebuginfo


Multiple patches

    auto_livepatch.sh -p example1.patch example2.patch ... exampleN.patch


Build module for Photon 3.0 aws flavor, with a set name and a set output directory

    auto_livepatch.sh -k 4.19.245-5.ph3-aws -p example.patch -n klp_module.ko -o livepatch_dir


Build module with description field

    auto_livepatch.sh -p example_patch -d description.txt

Package module as RPM

    auto_livepatch.sh -p example_patch -d description.txt -k 5.10.118-3.ph3 --rpm --rpm-version 2 --rpm-release 3 --rpm-desc rpm_description.txt

Photon 4.0 rt flavor - All options set

    auto_livepatch.sh -p example_patches/example.patch -k 5.10.118-rt67-3.ph4-rt -o test_dir -n test -d description.txt -R --export-debuginfo

****** gen_livepatch.sh ******

gen_livepatch builds a livepatch on your machine. This will work for building different flavors of the same Photon OS version (3.0 and above) as your machine, but there will likely be issues with cross compiling between different versions of Photon, as the core toolchain packages differ.

gen_livepatch [options] -p [list of patch files]

Options:

-k: Specifies the kernel version. If not set, uses uname -r
-p: Patch file list. Need at least one patch file listed here
-n: Output file name. Will be default if not specified.
-o: Output directory. Will be default if not specified.
-R: Disable replace flag (replace flag is on by default)
-d: Use file contents as description field for livepatch module.
-s: Specify the path to a local source rpm
-v: Specify the path to a local debuginfo rpm
--export-debuginfo: Saves debug files after module is built.
--rpm: Package the module inside of an rpm.
--rpm-version: Set the version number for the rpm.
--rpm-release: Set the release number for the rpm.
--rpm-desc: Set a separate description for the rpm. Input is a file.
-h/--help: Prints help message and exits

**Examples **

Simplest Usage - Build livepatch for current kernel.

    gen_livepatch.sh -p example.patch


Set non-replace flag and save debug information.

    gen_livepatch.sh -p example.patch -R --exportdebuginfo


Multiple patches.

    gen_livepatch.sh -p example1.patch example2.patch ... exampleN.patch


Build module with description field

    gen_livepatch.sh -p example_patch -d description.txt

Package module as RPM

    gen_livepatch.sh -p example_patch -d description.txt -k 5.10.118-3.ph3 --rpm --rpm-version 2 --rpm-release 3 --rpm-desc rpm_description.txt

Native module - All options set.

    gen_livepatch.sh -p example_patches/example.patch -o test_dir -n test -d description.txt -R --export-debuginfo

Specify kernel version (will fail if Photon versions don't match)

    gen_livepatch.sh -k 4.19.245-5.ph3-aws -p example.patch
