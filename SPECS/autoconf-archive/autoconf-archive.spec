%define debug_package %{nil}

Summary:        Autoconf macro archive
Name:           autoconf-archive
Version:        2022.09.03
Release:        2%{?dist}
URL:            http://www.gnu.org/software/autoconf-archive
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2022.09.03-2
- Release bump for SRP compliance
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2022.09.03-1
- Upgrade to v2022.09.03
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2021.02.19-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2019.01.06-1
- Automatic Version Bump
* Mon Sep 10 2018 Anish Swaminathan <anishs@vmware.com> 2018.03.13-1
- Initial build
