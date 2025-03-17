Summary:       Project Calico fork of the BIRD Internet Routing Daemon
Name:          calico-bird
Version:       0.3.3
Release:       4%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
URL:           https://github.com/projectcalico/bird
Distribution:  Photon

Source0:       %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:        calico-bird-gcc-10.patch

BuildRequires: autoconf
BuildRequires: bison

%description
Project Calico fork of the BIRD Internet Routing Daemon.

%prep
%autosetup -p1 -n bird-%{version} -p1

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
make clean %{?_smp_mflags}

%configure \
    --with-protocols="bgp pipe static" \
    --enable-client=no \
    --enable-pthreads=yes
make %{?_smp_mflags}
rm bird
make CC="gcc -static" %{?_smp_mflags}
cp bird dist/bird

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/bird6
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/birdcl

#%%check
# No tests available for this pkg

%files
%defattr(-,root,root)
%{_bindir}/bird
%{_bindir}/bird6
%{_bindir}/birdcl

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.3.3-4
- Release bump for SRP compliance
* Tue Sep 07 2021 Keerthana K <keerthanak@vmware.com> 0.3.3-3
- Bump up version to compile with new glibc
* Fri Jan 15 2021 Alexey Makhalov <amakhalov@vmware.com> 0.3.3-2
- GCC-10 support.
* Tue Jun 23 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.3-1
- Automatic Version Bump
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.3.1-2
- Use standard configure macros
* Wed Aug 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.3.1-1
- Calico BIRD routing daemon for PhotonOS.
