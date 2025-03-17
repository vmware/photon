Summary:        rt-tests tests various real-time features of linux
Name:           rt-tests
Version:        2.4
Release:        3%{?dist}
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/
Source0:        %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  build-essential
BuildRequires:  libnuma-devel
BuildRequires:  python3-devel
Requires:       python3
Requires:       libnuma
Requires:       glibc

%description
rt-tests includes various programs that test different real-time
features of the linux kernel. Refer to documentation on each test
for detailed descriptions.

%prep
%autosetup -n %{name}-%{version}

%build
%make_build prefix=%{_prefix}

%install
%make_install %{?_smp_mflags} prefix=%{_prefix}
ln -s %{python3_sitelib}/get_cyclictest_snapshot.py %{_bindir}/get_cyclictest_snapshot
ln -s %{python3_sitelib}/hwlatdetect.py %{_bindir}/hwlatdetect

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{python3_sitelib}/hwlatdetect.py
%{python3_sitelib}/get_cyclictest_snapshot.py
%{_mandir}/man8/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.4-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.4-2
- Update release to compile with python 3.11
* Thu Sep 08 2022 Sharan Turlapati <sturlapati@vmware.com> 2.4-1
- Initial version of rt-tests for Photon
