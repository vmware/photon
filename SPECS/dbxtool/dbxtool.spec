Summary:      Tool for managing dbx updates installed on a machine.
Name:         dbxtool
Version:      8
Release:      3%{?dist}
URL:          https://github.com/rhboot/dbxtool
Group:        System Environment/System Utilities
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://github.com/rhboot/dbxtool/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}
Patch0:        0001-dbxtool-Don-t-apply-unless-force-if-PK-or-KEK-are-un.patch
Patch1:        0003-Treat-dbxtool-a-dir-with-an-empty-directory-correctl.patch
Patch2:        0006-fix-relop-in-esl_iter_next.patch
Patch3:        0001-Fix-build-with-efivar-38.patch
BuildRequires: popt-devel efivar-devel systemd-rpm-macros
Requires:      efivar
%description
Tool for managing dbx updates installed on a machine.

%prep
%autosetup -p1
%build
%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}/etc \
       %{buildroot}/%{_datadir}/%{name}/DBXUpdate-2016-08-09-13-16-00.bin

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_docdir}/%{name}/COPYING
%{_mandir}/man1/%{name}.1.gz

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 8-3
- Release bump for SRP compliance
* Wed Feb 22 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 8-2
- Fix build with efivar 38
* Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 8-1
- Initial build. First version
