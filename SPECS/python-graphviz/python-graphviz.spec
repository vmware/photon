Summary:        Graph visualization dot render
Name:           python3-graphviz
Version:        0.20.1
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/graphviz
#wget https://github.com/xflr6/graphviz/archive/0.8.tar.gz -O graphviz-0.8.tar.gz
Source0:        graphviz-%{version}.zip

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  unzip
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
This package facilitates the creation and rendering of graph descriptions in the DOT language of the Graphviz graph drawing software (repo) from Python.

%prep
%autosetup -n graphviz-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.20.1-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.20.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.20.1-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.2-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.9-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.9-1
- Update to version 0.9
* Thu Jul 13 2017 Divya Thaluru <dthaluru@vmware.com> 0.8-1
- Initial packaging for Photon
