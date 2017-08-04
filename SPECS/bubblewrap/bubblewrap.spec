Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.1.8
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/projectatomic/bubblewrap
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/projectatomic/bubblewrap/releases/download/v%{version}/bubblewrap-%{version}.tar.xz
%define sha1    bubblewrap=02fed0d0f7402b18d63fef721fd242e942180715
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
%build

./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
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
*   Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.8-1
-   Initial build.  First version
