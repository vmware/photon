Name:           python3-deepmerge
Version:        0.2.1
Release:        1%{?dist}
Summary:        Python toolset to deeply merge python dictionaries.
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.org/project/deepmerge
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pypi.python.org/packages/source/n/deepmerge/deepmerge-%{version}.tar.gz
%define sha1    deepmerge=537f9701b5c94494589904873d92d1d54d059565

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  curl-devel
BuildRequires:  python3-pyparsing
BuildRequires:  python3-pip

%if 0%{?with_check:1}
BuildRequires:  python3-pytest
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-six
BuildRequires:  python3-requests
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A tools to handle merging of nested data structures in python.

%prep
%autosetup -p1 -n deepmerge-%{version}

%build
%py3_build

%install
%py3_install

%check
%if 0%{?with_check:1}
pushd deepmerge/tests/
pip3 install pluggy more-itertools funcsigs
pytest3
popd
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.2.1-1
- Bump version as a part of requests & chardet upgrade
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.1.1-2
- Update release to compile with python 3.10
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.0.5-3
- Mass removal python2
* Tue Apr 07 2020 Tapas Kundu <tkundu@vmware.com> 0.0.5-2
- Use photon bundled pyparsing for building deepmerge.
* Tue Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.0.5-1
- Initial packaging for photon OS
