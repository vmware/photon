%global commit_id 603cae8

Summary:        libnss-ato
Name:           libnss-ato
Version:        20201005
Release:        1%{?dist}
License:        GNU General Public License
URL:            https://github.com/donapieppo/libnss-ato
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 %{name}=f9583d8ec91644e6528bb4e9824682d1266895c7bce2784a7fcaf29ad155fb6ac83359cd996cf3fd03b114d4363ff341e58fee730520f278422b4dffcbc2c85e

Source1: %{name}.conf

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
mkdir -p %{buildroot}{%{_libdir},%{_sysconfdir}}
mv libnss_ato*.so* %{buildroot}%{_libdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}

%check
./libnss_ato_test root

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_libdir}/libnss_ato*.so*

%changelog
* Fri Mar 29 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20201005-1
- Re-introduce libnss-ato (https://github.com/donapieppo/libnss-ato/issues/21)
- Kept changelog intact from Ph4
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-3
- Ensure non empty debuginfo
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.6-2
- GA - Bump release of all rpms
* Wed Oct 28 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging. First version
