Name:           python3-prometheus_client
Version:        0.14.1
Release:        2%{?dist}
Summary:        Python client for the Prometheus monitoring system.
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/prometheus_client
Source0: prometheus_client-%{version}.tar.gz
%define sha512  prometheus_client=3ba1389f23566ecab1371452ec717e06c4e444d1ac8a37cb27429493e64f3931e6876734c0947cb43ba086ed51ca47a0c7764d488ea6e7f2d0864447f49b09e4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
Python client for the Prometheus monitoring system.

%prep
%autosetup -p1 -n prometheus_client-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py tests
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.14.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.8.0-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.3.1-3
- Mass removal python2
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 0.3.1-2
- Fix make check
- uploaded test source
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.3.1-1
- Update to version 0.3.1
* Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 0.0.20-2
- fix make check issue by using upstream sources
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.0.20-1
- Initial version of python-prometheus_client package for Photon.
