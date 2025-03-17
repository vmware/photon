%global commit_id       574c5ab
%define debug_package   %{nil}

Summary:        libnss-ato
Name:           libnss-ato
Version:        20240514
Release:        4%{?dist}
URL:            https://github.com/donapieppo/libnss-ato
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz

Source1: %{name}.conf
Source2: %{name}-allowed-progs.conf

Source3: license.txt
%include %{SOURCE3}

Patch0: 0001-allow-only-desired-programs.patch

Provides: libnss_ato = %{version}-%{release}

Requires: nss

BuildRequires: nss-devel

%if 0%{?with_check}
BuildRequires: shadow
%endif

%description
The libnss_ato module is a set of C library extensions,
which allows to map every nss request for unknown user to a single predefined user.

%prep
%autosetup -p1 -n %{name}-%{commit_id}

%build
%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_mandir}

cp %{SOURCE1} \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}

%check
./libnss_ato_test root

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/%{name}.conf
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/%{name}-allowed-progs.conf
%{_libdir}/libnss_ato*.so*

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 20240514-4
- Release bump for SRP compliance
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20240514-3
- Remove an error log which was intervening with bash completion
* Tue Jul 09 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20240514-2
- Disable debuginfo rpm build
* Tue May 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20240514-1
- Upgrade to latest
- Allow only desired programs
* Fri Mar 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20201005-1
- Re-introduce libnss-ato (https://github.com/donapieppo/libnss-ato/issues/21)
- Kept changelog intact from Ph4
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-3
- Ensure non empty debuginfo
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-2
- GA - Bump release of all rpms
* Wed Oct 28 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging. First version
