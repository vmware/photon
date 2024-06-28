# Building Package or Kernel Modules Using a Script

You can use a script to build a single Photon OS package without rebuilding all Photon OS packages. You just need a `.spec` specification file and sources. You place the sources and the specification files in the same folder and run the `build_spec.sh` script. The script performs the following steps:

- Creates sandbox using docker.
- Installs build tools and `.spec` build requirements from the Photon OS repository.
- Runs `rpmbuild`.

**Result:** You have a native Photon OS RPM package.

The `build-spec.sh` script is located in the `photon/tools/scripts/` folder.

- [Prerequisties](#prerequisites)
- [Procedure](#procedure)
- [Example](#example)
- [Build Logs](#build-logs)

## Prerequisites

Before you run the `build-spec.sh` script, perform the following steps:

- Ensure you have any Linux OS with docker daemon running.
- Place the source and RPM `.spec` files in the same folder, that is, `$WORKDIR`.

## Procedure

Run the script. Provide the RPM `.spec` file name, including absolute or relative path, as argument:

```
./photon/tools/scripts/build_spec.sh <$WORKDIR/rpm_spec_file.spec>
```

The RPMs and full build logs are generated in the `$WORKDIR/stage` folder.

## Example

The following example runs the script with `simple-module.spec` as argument, where `simple-module.spec` is the specification file:

```
./photon/tools/scripts/build_spec.sh ~/photon/tools/examples/build_spec/simple-module.spec
```

The following are the contents of the `simple-module.spec` file:

```
Summary:        Simple Linux module
Name:           simple-module
Version:        4.18.9
Release:        5%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        module_example.tar.xz
BuildRequires:  linux-devel = 4.18.9
BuildRequires:  kmod
Requires:       linux = 4.18.9

%description
Example of building linux module for Photon OS

%prep
%setup -q -n module_example

%build
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` VERBOSE=1 modules %{?_smp_mflags}

%install
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
# fix permissins to generate non empty debuginfo
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%post
/sbin/depmod -a

%files
%defattr(-,root,root)
/lib/modules/*

```

## Build Logs

The followiing logs indicate the steps that the script performs internally:

```
1. Create sandbox
	Use local build template image OK
2. Prepare build environment
	Create source folder OK
	Copy sources from <HOME>/photon/tools/examples/build_spec/simple-module OK
	Install build requirements OK
3. Build
	Run rpmbuild OK
4. Get binaries
	Copy RPMS OK
	Copy SRPMS OK
5. Destroy sandbox
	Stop container OK
	Remove container OK

Build completed. RPMS are in '<HOME>/photon/tools/examples/build_spec/simple-module/stage' folder
```

