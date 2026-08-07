%global debug_package %{nil}
%define TINI_GITCOMMIT de40ad0

Name:           tini
Version:        0.19.0
Release:        2%{?dist}
Summary:        A tiny but valid init for containers
Vendor:         VMware, Inc.
Group:          System Environment/Base
Distribution:   Photon
URL:            https://github.com/krallin/tini
Source0:        https://github.com/krallin/tini/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# tini's CMakeLists.txt overwrites tini_VERSION_GIT and git_version_check_ret
# from execute_process(), which clobbers the -D values passed below. An RPM
# builds from a tarball with no .git, so the git call fails and the version
# suffix is silently dropped, leaving `docker info` with an empty init version.
# This patch disables the git invocation so the -D values take effect.
Patch0:         tini-disable-git.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel

%description
Tini is a trivial implementation for an "init" program.
All Tini does is spawn a single child (Tini is meant to be run in a container),
and wait for it to exit, all the while reaping zombies and performing signal forwarding.
libc will be needed inside the container.

%package        static
Summary:        Standalone static build of tini

%description    static
Statically linked build of tini, meant to be used inside a container.
Because this binary carries no dynamic dependencies it can be bind-mounted
into a container built against any libc (glibc, musl) or into one with no
libc at all, which is what the container runtime requires of an init that
it injects from the host.

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

%files static
%defattr(-,root,root,-)
%{_bindir}/tini-static

%changelog
* Fri Aug 07 2026 Daniel Casota <dcasota@gmail.com> 0.19.0-2
- Ship tini-static in a new subpackage instead of discarding it
- Restore tini-disable-git.patch so the version suffix is not dropped
* Tue Apr 08 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 0.19.0-1
- Initial build
