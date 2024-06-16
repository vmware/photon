Name:       rpmdevtools
Version:    9.6
Release:    3%{?dist}
Summary:    RPM Development Tools
License:    GPLv2+ and GPLv2
URL:        https://pagure.io/rpmdevtools
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Tools

Source0: https://releases.pagure.org/rpmdevtools/%{name}-%{version}.tar.xz
%define sha512 %{name}=691fec8944029dbe60cb3eab0200d1201f5aa3dd11cd49e8313ee7c1fe998237217ea9c5ae7b4a70f61f3c998093f23d26266b23f41607ddca3148d5f6b6ae06

Patch0: 0001-rpmdev-spectool-remove-progressbar-support.patch

BuildArch: noarch

BuildRequires: help2man
BuildRequires: python3-rpm
BuildRequires: build-essential
BuildRequires: python3-devel
BuildRequires: perl
BuildRequires: python3-requests

Requires: curl
Requires: diffutils
Requires: file
Requires: findutils
Requires: gawk
Requires: grep
Requires: rpm-build
Requires: python3-rpm
Requires: sed

%description
This package contains scripts to help in development of RPM packages.
rpmdev-setuptree    Create RPM build tree within user's home directory
rpmdev-diff         Diff contents of two archives
rpmdev-newspec      Creates new .spec from template
rpmdev-rmdevelrpms  Find (and optionally remove) "development" RPMs
rpmdev-checksig     Check package signatures using alternate RPM keyring
rpminfo             Print information about executables and libraries
rpmdev-md5/sha*     Display checksums of all files in an archive file
rpmdev-vercmp       RPM version comparison checker
rpmdev-spectool     Expand and download sources and patches in specfiles
rpmdev-wipetree     Erase all files within dirs created by rpmdev-setuptree
rpmdev-extract      Extract various archives, "tar xvf" style
rpmdev-bumpspec     Bump revision in specfile
...and many more.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
mv %{buildroot}%{_sysconfdir}/bash_completion.d/* \
        %{buildroot}%{_datadir}/bash-completion/completions/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpmdevtools/
%{_datadir}/rpmdevtools/
%{_bindir}/*
%{_mandir}/*
%{_datadir}/bash-completion/*

%changelog
* Sun Jun 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.6-3
- Bump version as a part of rpm upgrade
* Mon Nov 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.6-2
- Bump version as a part of rpm upgrade
* Tue Mar 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.6-1
- Initial version.
