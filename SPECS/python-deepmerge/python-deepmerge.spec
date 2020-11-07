%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-deepmerge
Version:        0.1.1
Release:        1%{?dist}
Summary:        Python toolset to deeply merge python dictionaries.
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.org/project/deepmerge
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/deepmerge/deepmerge-%{version}.tar.gz
%define sha1    deepmerge=b8e46f599bc7db522356fbc556cde08dbe75900a
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  curl-devel
BuildRequires:  python3-pyparsing
%if %{with_check}
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
%setup -q -n deepmerge-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pushd ../p3dir/deepmerge/tests/
pip3 install pluggy
pip3 install more-itertools
pip3 install funcsigs
pytest3
popd

%clean
rm -rf %{buildroot}/*


%files
%defattr(-,root,root)
%doc README.rst
%{python3_sitelib}/*

%changelog
*  Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
-  Automatic Version Bump
*  Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.0-1
-  Automatic Version Bump
*  Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.0.5-3
-  Mass removal python2
*  Tue Apr 07 2020 Tapas Kundu <tkundu@vmware.com> 0.0.5-2
-  Use photon bundled pyparsing for building deepmerge.
*  Tue Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.0.5-1
-  Initial packaging for photon OS
