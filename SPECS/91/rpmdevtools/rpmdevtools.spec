%global build_if %{photon_subrelease} <= 91

Name:       rpmdevtools
Version:    9.6
Release:    1.1%{?dist}
Summary:    RPM Development Tools
URL:        https://pagure.io/rpmdevtools
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Tools

Source0: https://releases.pagure.org/rpmdevtools/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 9.6-1.1
- Bump after moving to SPECS/91
* Mon Sep 22 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 9.6-1
- Initial version.
