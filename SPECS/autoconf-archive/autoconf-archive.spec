%define debug_package %{nil}

Summary:        Autoconf macro archive
Name:           autoconf-archive
Version:        2022.09.03
Release:        1%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/autoconf-archive
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha512 %{name}=157b5b6a979d5ec5bfab6ddf34422da620fec1e95f4c901821abbb7361544af77747b4a449029b84750d75679d6130a591e98da8772de2c121ecdea163f0340b

BuildArch:      noarch

Requires:       autoconf

%description
The package contains programs for producing shell scripts that can automatically configure source code.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{_smp_mflags} INSTALL="install -p"
rm -rf %{buildroot}%{_infodir}
# doc and license files are installed elsewhere
rm -frv %{buildroot}%{_docdir}/%{name}

%files
%defattr(-,root,root)
%{_datadir}/aclocal/*.m4

%changelog
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2022.09.03-1
- Upgrade to v2022.09.03
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2021.02.19-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2019.01.06-1
- Automatic Version Bump
* Mon Sep 10 2018 Anish Swaminathan <anishs@vmware.com> 2018.03.13-1
- Initial build
