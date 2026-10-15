Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.4.1
Release:        2%{?dist}
License:        LGPLv2+
URL:            https://github.com/projectatomic/bubblewrap
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/projectatomic/bubblewrap/releases/download/v%{version}/bubblewrap-%{version}.tar.xz
%define sha512  %{name}=0ff46dc0fda2d0cffbb36cc52ff43951b30cbd835a42cc56806acbbbd827796bfadbb1cfafc84d6b47a72c031ca44abe1c377acc0cc25fe3b33e854f5f687d35

# Add --bind-fd support required for CVE-2024-42472
Patch1:         CVE-2024-42472.patch
# Fix existing nested PID namespace test under container builds
Patch2:         fix-pid-namespace-test.patch
# Use the supported Python interpreter for tests
Patch3:         use-python3-in-tests.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libcap-devel
%if 0%{?with_check}
# Test requirements
BuildRequires:  util-linux
BuildRequires:  python3
%endif

Requires:       libcap

%description
Bubblewrap could be viewed as setuid implementation of a subset of user namespaces. Emphasis on subset - specifically relevant to the above CVE, bubblewrap does not allow control over iptables.

The original bubblewrap code existed before user namespaces - it inherits code from xdg-app helper which in turn distantly derives from linux-user-chroot.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --with-priv-mode=none
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/bwrap
%{_datadir}/bash-completion/completions/bwrap

%changelog
* Thu Oct 15 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 0.4.1-2
- Add --bind-fd support for CVE-2024-42472
- Backport upstream test corrections and declare test requirements
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.1-1
- Automatic Version Bump
* Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 0.3.0-1
- Updated to version 0.3.0.
* Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.8-1
- Initial build.  First version
