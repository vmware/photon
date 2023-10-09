Summary:          Programs for basic networking
Name:             iputils
Version:          20180629
Release:          4%{?dist}
License:          BSD-3 and GPLv2+
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: %{name}-s%{version}.tar.gz
%define sha512 %{name}=16b8f5ad1cf88083ebaee0a71fddb14bb0a904336fd0baebfcca86c27ac0773553b21d12790b05cab7661d6432c75bbb1523e871e5e1b77faacd13ccc84f4476

BuildRequires:    libcap-devel
BuildRequires:    libgcrypt-devel

Requires:         libcap
Requires:         libgcrypt

Obsoletes:        inetutils

%description
The Iputils package contains programs for basic networking.

%prep
%autosetup -p1 -n %{name}-s%{version}

%build
%make_build USE_IDN=no USE_GCRYPT=yes

pushd ninfod
%configure
%make_build
popd

%install
mkdir -p %{buildroot}{%{_sbindir},%{_bindir},%{_unitdir}}

install -c clockdiff %{buildroot}%{_sbindir}/
install -cp arping %{buildroot}%{_sbindir}/
install -cp ping %{buildroot}%{_bindir}/
install -cp rdisc %{buildroot}%{_sbindir}/
install -cp tracepath %{buildroot}%{_bindir}/
install -cp traceroute6 %{buildroot}%{_bindir}/
install -cp ninfod/ninfod %{buildroot}%{_sbindir}/

ln -sf ping %{buildroot}%{_bindir}/ping6
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}
ln -sf ../bin/traceroute6 %{buildroot}%{_sbindir}

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
* Mon Oct 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 20180629-4
- Use relative path for ping6 symlink
* Tue Dec 22 2020 Shreenidhi Shedi <sshedi@vmware.com> 20180629-3
- Bump version as a part of autospec library upgrade
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
