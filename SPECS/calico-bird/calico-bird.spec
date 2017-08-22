Summary:       Project Calico fork of the BIRD Internet Routing Daemon
Name:          calico-bird
Version:       0.3.1
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       GPL
URL:           https://github.com/projectcalico/bird
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: ncurses-devel
Requires:      ncurses
%define sha1 calico-bird=51734c2d53fa60f06f02ba4d64c41968090f99ef

%description
Project Calico fork of the BIRD Internet Routing Daemon.

%prep
%setup -q -n bird-0.3.1

%build
mkdir -p dist
autoconf
# IPv6 bird + bird client
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --with-protocols="bgp pipe static" \
    --enable-ipv6=yes \
    --enable-client=yes \
    --enable-pthreads=yes
make
# Remove the dynmaic binaries and rerun make to create static binaries
rm bird birdcl
make CC="gcc -static"
cp bird dist/bird6
cp birdcl dist/birdcl
# IPv4 bird
make clean
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --with-protocols="bgp pipe static" \
    --enable-client=no \
    --enable-pthreads=yes
make
rm bird
make CC="gcc -static"
cp bird dist/bird

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird6
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/birdcl

%files
%defattr(-,root,root)
%{_bindir}/bird
%{_bindir}/bird6
%{_bindir}/birdcl

%changelog
*    Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.1-1
-    Calico BIRD routing daemon for PhotonOS.
