Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.3.0
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://github.com/projectatomic/bubblewrap
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/projectatomic/bubblewrap/releases/download/v%{version}/bubblewrap-%{version}.tar.xz
%define sha1    bubblewrap=74a3c0f2942935be4ae6f82b43d59fdc9de92e83
Patch0:         bubblewrap-CVE-2019-12439.patch
Patch1:         bubblewrap-CVE-2020-5291.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libcap-devel
Requires:       libcap
%description
Bubblewrap could be viewed as setuid implementation of a subset of user namespaces. Emphasis on subset - specifically relevant to the above CVE, bubblewrap does not allow control over iptables.

The original bubblewrap code existed before user namespaces - it inherits code from xdg-app helper which in turn distantly derives from linux-user-chroot.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
    --disable-silent-rules \
    --with-priv-mode=none
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/bwrap
%{_datadir}/bash-completion/completions/bwrap

%changelog
*   Mon Apr 06 2020 Ankit Jain <ankitja@vmware.com> 0.3.0-3
-   Fix for CVE-2020-5291
*   Mon Jun 10 2019 Ankit Jain <ankitja@vmware.com> 0.3.0-2
-   Fix for CVE-2019-12439
*   Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 0.3.0-1
-   Updated to version 0.3.0.
*   Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.8-1
-   Initial build.  First version
