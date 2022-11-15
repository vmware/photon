Name:           python3-prometheus_client
Version:        0.8.0
Release:        2%{?dist}
Summary:        Python client for the Prometheus monitoring system.
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/prometheus_client
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: prometheus_client-%{version}.tar.gz
%define sha512 prometheus_client=76f548b77bcb3630ac069cc4004bffd44fdebc600beefbd390ad06e53c61bc743840cda0fc349e876cd5cf8f915000ac2432da3d4698f6e7d73f77ead7b2b400

Source1: client_python-tests-%{version}.tar.gz
%define sha512 client_python-tests=d4c6e2cd633ef31a47f644c83eb41446dced191cd49e137cddc2301bc872312bae9b07c63e840c1aa666f7037c80aa6ed64246ee63a036406e4d9a69caa3e15b

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
tar xf %{SOURCE1} --no-same-owner

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
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
