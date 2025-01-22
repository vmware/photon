Summary:          Programs for basic networking
Name:             iputils
Version:          20200821
Release:          4%{?dist}
License:          BSD-3 and GPLv2+
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: %{name}-s%{version}.tar.gz
%define sha512 %{name}=4a57c3637cdd9aab2600682774e27370716cbdf1c7ac8ae61bf86c21c08701a5b697792df4aa95309b196eaa74f3cb6b2836a40f04da0e602156e982ac99d8c9

BuildRequires:    libcap-devel
BuildRequires:    libgcrypt-devel
BuildRequires:    ninja-build
BuildRequires:    meson

Requires:         libcap
Requires:         libgcrypt

Obsoletes:        inetutils

%description
The Iputils package contains programs for basic networking.

%prep
%autosetup -p1 -n %{name}-s%{version}

%build
meson \
  --prefix %{_usr} \
  --buildtype=plain builddir \
  -DUSE_IDN=false \
  -DBUILD_MANS=false \
  -DBUILD_TRACEROUTE6=true

ninja -v -C builddir

%install
mkdir -p %{buildroot}{%{_sbindir},%{_bindir},%{_unitdir}}

pushd builddir
install -c clockdiff %{buildroot}%{_sbindir}/
install -cp arping %{buildroot}%{_sbindir}/
install -cp ping/ping %{buildroot}%{_bindir}/
install -cp rdisc %{buildroot}%{_sbindir}/
install -cp tracepath %{buildroot}%{_bindir}/
install -cp traceroute6 %{buildroot}%{_bindir}/
install -cp ninfod/ninfod %{buildroot}%{_sbindir}/

ln -sf ping %{buildroot}%{_bindir}/ping6
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}
ln -sf ../bin/traceroute6 %{buildroot}%{_sbindir}
popd

cp Documentation/RELNOTES.old ./
iconv -f ISO88591 -t UTF8 RELNOTES.old -o RELNOTES.tmp
touch -r RELNOTES.old RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES.old

%files
%defattr(-,root,root)
%doc RELNOTES.old
%{_sbindir}/rdisc
%{_sbindir}/ninfod
%{_sbindir}/tracepath
%{_sbindir}/traceroute6
%{_bindir}/tracepath
%{_bindir}/traceroute6
%caps(cap_net_raw=p) %{_sbindir}/clockdiff
%caps(cap_net_raw=p) %{_sbindir}/arping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping6

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 20200821-4
- Bump version as a part of meson upgrade
* Mon Oct 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 20200821-3
- Use relative path for ping6 symlink
* Tue Nov 01 2022 Piyush Gupta <gpiyush@vmware.com> 20200821-2
- Removed unknown option -DUSE_GCRYPT after meson upgrade.
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20200821-1
- Automatic Version Bump
* Wed Aug 12 2020 Tapas Kundu <tkundu@vmware.com> 20190709-2
- Fix variable name collision with libcap update
* Mon Jul 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20190709-1
- Automatic Version Bump
* Thu Oct 10 2019 Tapas Kundu <tkundu@vmware.com> 20180629-2
- Provided ping6 as symlink of ping
* Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 20180629-1
- Updated to version 20180629
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 20151218-4
- Remove openssl and gnutls deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20151218-3
- GA - Bump release of all rpms
* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 20151218-2
- Fixing permissions for binaries
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 20151218-1
- Updated to version 2.4.18
* Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 20121221-1
- Initial build.    First version
