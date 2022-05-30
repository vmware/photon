Summary:        Manage dynamic plugins for Python applications
Name:           python3-stevedore
Version:        3.5.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://opendev.org/openstack/stevedore
Source0:        https://tarballs.openstack.org/stevedore/stevedore-%{version}.tar.gz
%define sha512  stevedore=be0f82230d7d4d3cf18dd913e11093ad90744e32a3021d9f88f0be244f56d0e3606af0adef67674c569c41d885837be3f0fc4d58009e036151cc67963a4f2ab3

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-attrs
BuildRequires:  python3-docutils
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-sphinx
%endif

Requires:       python3

%description
Python makes loading code dynamically easy, allowing you to configure and extend your application
by discovering and loading extensions ("plugins") at runtime. Many applications implement their
own library for doing this, using __import__ or importlib.
stevedore avoids creating yet another extension mechanism by building on top of setuptools entry points.
The code for managing entry points tends to be repetitive, though, so stevedore provides manager classes
for implementing common patterns for using dynamically loaded extensions.

%prep
%autosetup -n stevedore-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install pluggy atomicwrites funcsigs more_itertools testtools
python3 -m pytest stevedore/tests -k "not test_extension"
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.5.0-1
- Python stevedore initial build
