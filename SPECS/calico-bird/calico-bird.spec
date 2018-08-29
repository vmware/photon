Summary:       Project Calico fork of the BIRD Internet Routing Daemon
Name:          calico-bird
Version:       0.3.1
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPL
URL:           https://github.com/projectcalico/bird
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: autoconf
%define sha1 calico-bird=51734c2d53fa60f06f02ba4d64c41968090f99ef

%description
Project Calico fork of the BIRD Internet Routing Daemon.

%prep
%setup -q -n bird-0.3.1

%build
mkdir -p dist
autoconf
# IPv6 bird + bird client
%configure \
    --with-protocols="bgp pipe static" \
    --enable-ipv6=yes \
    --enable-client=yes \
    --enable-pthreads=yes
make %{?_smp_mflags}
# Remove the dynmaic binaries and rerun make to create static binaries
rm bird birdcl
make %{?_smp_mflags} CC="gcc -static"
cp bird dist/bird6
cp birdcl dist/birdcl
# IPv4 bird
make clean
%configure \
    --with-protocols="bgp pipe static" \
    --enable-client=no \
    --enable-pthreads=yes
make %{?_smp_mflags}
rm bird
make CC="gcc -static"
cp bird dist/bird

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird6
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/birdcl

#%check
# No tests available for this pkg

%files
%defattr(-,root,root)
%{_bindir}/bird
%{_bindir}/bird6
%{_bindir}/birdcl

%changelog
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.1-2
-   Use standard configure macros
*   Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.1-1
-   Calico BIRD routing daemon for PhotonOS.
