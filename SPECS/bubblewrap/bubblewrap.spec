Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.7.0
Release:        2%{?dist}
URL:            https://github.com/projectatomic/bubblewrap
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/projectatomic/bubblewrap/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libcap-devel

Requires:       libcap

%description
Bubblewrap could be viewed as setuid implementation of a subset of user namespaces. Emphasis on subset - specifically relevant to the above CVE, bubblewrap does not allow control over iptables.
The original bubblewrap code existed before user namespaces - it inherits code from xdg-app helper which in turn distantly derives from linux-user-chroot.

%prep
%autosetup -p1

%build
sh autogen.sh
%configure \
    --disable-silent-rules \
    --with-priv-mode=none
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/bwrap
%{_datadir}/bash-completion/completions/bwrap
%{_datadir}/zsh/site-functions/_bwrap

%changelog
*   Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.7.0-2
-   Release bump for SRP compliance
*   Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 0.7.0-1
-   Automatic Version Bump
*   Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 0.6.2-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.1-1
-   Automatic Version Bump
*   Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 0.3.0-1
-   Updated to version 0.3.0.
*   Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.8-1
-   Initial build.  First version
