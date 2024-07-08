%global commit_id       574c5ab
%define debug_package   %{nil}

Summary:        libnss-ato
Name:           libnss-ato
Version:        20240514
Release:        1%{?dist}
License:        GNU General Public License
URL:            https://github.com/donapieppo/libnss-ato
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=506e0fa07c4d67e9e2d2f6f101bcd0e8c21c60e60cfa92c3cc7e81577655e68da4f4cfd14a361e9897947f6b5aa0752f5cacec0d519289550188789cb2e28ddd

Source1: %{name}.conf
Source2: %{name}-allowed-progs.conf

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
