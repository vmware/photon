%global debug_package %{nil}
%define TINI_GITCOMMIT de40ad0

Name:           tini
Version:        0.19.0
Release:        1%{?dist}
Summary:        A tiny but valid init for containers
Vendor:         VMware, Inc.
Group:          System Environment/Base
Distribution:   Photon
URL:            https://github.com/krallin/tini
Source0:        https://github.com/krallin/tini/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel

%description
Tini is a trivial implementation for an "init" program.
All Tini does is spawn a single child (Tini is meant to be run in a container),
and wait for it to exit, all the while reaping zombies and performing signal forwarding.
libc will be needed inside the container.

%prep
%autosetup -p1 -c

%build
CFLAGS="${CFLAGS-} -DPR_SET_CHILD_SUBREAPER=36 -DPR_GET_CHILD_SUBREAPER=37"
export CFLAGS

%cmake \
    -Dtini_VERSION_GIT:STRING=%{TINI_GITCOMMIT} \
    -Dgit_version_check_ret=0

%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root,-)
%{_bindir}/tini
%exclude %{_bindir}/tini-static

%changelog
* Tue Apr 08 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 0.19.0-1
- Initial build
