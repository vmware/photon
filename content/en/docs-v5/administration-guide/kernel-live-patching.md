---
title:  Kernel Live Patching
weight: 10
---

Photon OS supports Kernel Live Patching updates to the kernel in the RT, AWS, and generic kernel flavors. With this feature, you can modify the currently running operating system without rebooting. For example, you can apply security fixes without interrupting or pausing running processes to upgrade the operating system.

Kernel Live Patching is supported on the x86 architecture, but not on the ARM architecture. Kernel Live Patching is also supported on other architectures, such as s390 and ppc64le, which are not compatible with Photon OS.

Kernel Live Patching is supported on the following Photon OS versions:


- Photon 5.0+ - all versions
- Photon 4.0 - 5.10.118-2 and later
- Photon 3.0 - 4.19.247-2 and later

## Installing packages ##

Kernel Live Patching in Photon OS is supported with `kpatch`. Kernel Live Patching capabilities are split into three subpackages:

1.	kpatch - basic loading, unloading, etc. of livepatch modules only
2.	kpatch-build - manually build livepatch modules
3.	kpatch-utils - tools to automate livepatch module building for Photon OS

You can install all packages by using the `tdnf` command:

```console
tdnf install kpatch kpatch-build kpatch-utils
```

## Building livepatch modules ##

To build livepatch modules, first install the kpatch-utils package through `tdnf`. Livepatch building functionality can be accessed through the auto_livepatch.sh tool. This tool can cross-build livepatch modules for any version of Photon OS, as well as package livepatch modules into rpm packages.

**Note:** If necessary, you can use kpatch-build alone to build livepatch modules for Photon, but it lacks much of the functionality of the auto_livepatch.sh tool.

Details on how to use the tool are listed below:

```console
auto_livepatch.sh [options] -p [list of patch files]
```

Options:

- -k: Specifies the kernel version. If not set, uses uname -r
- -p: Patch file list. Need at least one patch file listed here
- -n: Output file name. Will be default if not specified.
- -o: Output directory. Will be default if not specified.
- -R: Disable replace flag (replace flag is on by default)
- --export-debuginfo: Saves debug files after module is built.
- -d: Use specified file contents as the module's description field
- --rpm: Package the module inside of an rpm.
- --rpm-version: Set the version number for the rpm.
- --rpm-release: Set the release number for the rpm.
- --rpm-desc: Set a separate description for the rpm. Input is a file.
- -h/--help: Prints help message and exits


## Examples ##

The following examples show the syntax for various use case scenarios:

Simplest Usage - Build livepatch for current kernel.

```console
auto_livepatch.sh -p example.patch
```

Set description.

```console
auto_livepatch.sh -p example.patch -d description.txt
```

Set non-replace flag and save debug information.

```console
auto_livepatch.sh -p example.patch -R --exportdebuginfo
```

Multiple patches.

```console
auto_livepatch.sh -p example1.patch example2.patch ... exampleN.patch
```

Build module for Photon 3.0 aws flavor, with a set name and a set output directory.

```console
auto_livepatch.sh -k 4.19.245-5.ph3-aws -p example.patch -n klp_module.ko -o livepatch_dir
```

Photon 4.0 rt flavor - All options set.

```console
auto_livepauto_livepatch.sh -p example_patches/example.patch -k 5.10.118-rt67-3.ph4-rt -o test_dir -n test -d description.txt -R --export-debuginfoatch.sh -p example.patch
```

Package module as RPM - separate descriptions for the module and the rpm.

```console
auto_livepatch.sh -p example_patch -d description.txt -k 5.10.118-3.ph3 --rpm --rpm-version 0.6.9 --rpm-release 3 --rpm-desc rpm_description.txt
```

## Loading, unloading, and installing ##

You can use the following commands for the loading, unloading, and installing scenarios.

Loading:

```console
kpatch load livepatch_module.ko
```

 Unloading:

```console
kpatch unload livepatch_module
```

Livepatches will be loaded on boot if they are installed through the kpatch install command:

```console
kpatch install livepatch_module.ko
```

`kpatch install` will not load the module into the running kernel though, it will only be loaded on boot. To load a livepatch immediately, you must run `kpatch load`.

**Note:** The `systemd kpatch` service might fail to load livepatch modules on boot. You should verify that the `kpatch` service ran successfully. You can verify by running the `systemctl status kpatch` command, or by checking the logs at `dmesg/journalctl`.

To remove a livepatch from the list of livepatches to be loaded on boot, run:

```console
kpatch uninstall livepatch_module
```

As livepatches can be packaged into RPMs with `auto_livepatch.sh`, loading livepatch RPMs is done like any other rpm - with `tdnf`. Livepatch modules will be both installed (to be loaded on boot) and loaded into the running kernel.

```console
tdnf install livepatch.rpm
```

Uninstallation works like with any other rpm. You can uninstall by using the `tdnf` command.

## Inspecting livepatch information ##

You can run the following commands to retrieve useful information:

- `lsmod` - list currently loaded kernel modules. Loaded livepatch modules should appear here alongside regular kernel modules.
- `modinfo <module_name>` - print module information/description

## Management of livepatches - Update strategy ##

Photon OS (4.0 and later) supports atomic replace/cumulative updates of livepatch modules. This means that when you load in a new livepatch, it disables all of the older livepatch modules and only uses the new code. This is to avoid any conflicts that could arise from multiple livepatches interacting or modifying the same pieces of code. For more information, see [https://docs.kernel.org/livepatch/cumulative-patches.html](https://docs.kernel.org/livepatch/cumulative-patches.html).

Therefore, if you want to load more than one livepatch at one time, all of the patches must be consolidated into a single livepatch module. When loaded, the old module will be disabled and the new one will be enabled.

**Note:** Photon 3.0 does not automatically disable all older livepatches, so it is recommended to do this manually before loading the new cumulative patch.