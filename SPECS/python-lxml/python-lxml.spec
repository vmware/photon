Summary:        XML and HTML with Python
Name:           python3-lxml
Version:        4.9.1
Release:        3%{?dist}
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/lxml/lxml
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/lxml/lxml/archive/refs/tags/lxml-%{version}.tar.gz
%define sha512 lxml=d7ec55c7db2c63a716ca5f4d833706d90fc76c944885e010fcdb96786bcfe796994e438450cf4e8e6e75d702e21fb16971f28f854d7a1f76c34e4ae315414d84

BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel
BuildRequires:  cython3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       libxslt
Requires:       libxml2

%description
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.

%prep
%autosetup -p1 -n lxml-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
make %{?_smp_mflags} test
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.1-3
- Bump version as a part of libxml2 upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.9.1-2
- Bump version as a part of libxslt upgrade
* Mon Jul 18 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.1-1
- Upgrade to version 4.9.1
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.6.1-2
- Bump version as a part of libxslt upgrade
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 4.6.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.5.2-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 4.2.4-3
- Mass removal python2
* Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> 4.2.4-2
- Fix make check
- moved build requires from subpackage
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.4-1
- Update to version 4.2.4
* Mon Aug 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.7.3-3
- set LC_ALL and LANGUAGE for the tests to pass
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.7.3-2
- Use python2_sitelib
* Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 3.7.3-1
- Update to 3.7.3
* Wed Feb 08 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0b1-4
- Added python3 site-packages.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.5.0b1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.0b1-2
- GA - Bump release of all rpms
* Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 3.5.0b1-1
- Initial build.
