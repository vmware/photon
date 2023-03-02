%global debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           PyYAML
Version:        5.4.1
Release:        2%{?dist}
Summary:        YAML parser and emitter for Python
Group:          Development/Libraries
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{name}-%{version}.tar.gz
%define sha512 %{name}=359c45d843fd839797572efeab121f17b1947647960dfb062f3618f25f71e1a6bc4bab14a1720b6b67f256089d5d48c452ec5419e3130222765c7ca41db11dad

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  libyaml-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libyaml-devel
BuildRequires:  cython3

Requires:       python2
Requires:       libyaml

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that allow
to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistence.

%package -n     python3-PyYAML
Summary:        python3-PyYAML
Requires:       python3
Requires:       libyaml

%description -n python3-PyYAML
Python 3 version.

%prep
%autosetup -p1 -n %{name}-%{version}

rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
chmod a-x examples/yaml-highlight/yaml_hl.py
pushd ../p3dir
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
chmod a-x examples/yaml-highlight/yaml_hl.py
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc PKG-INFO README LICENSE examples
%{python2_sitelib}/*

%files -n python3-PyYAML
%defattr(-,root,root,-)
%doc PKG-INFO README LICENSE examples
%{python3_sitelib}/*

%changelog
* Thu Mar 02 2023 Nitesh Kumar <kunitesh@vmware.com> 5.4.1-2
- Adding Requires cython3 to build with binding libyaml
* Mon Feb 06 2023 Prashant S Chauhan <psinghchauha@vmware.com> 5.4.1-1
- Update to version 5.4
* Wed Jan 27 2021 Tapas Kundu <tkundu@vmware.com> 3.13-6
- Fix CVE-2020-14343
* Wed Apr 08 2020 Tapas Kundu <tkundu@vmware.com> 3.13-5
- Fix for CVE-2020-1747
* Sat Mar 07 2020 Tapas Kundu <tkundu@vmware.com> 3.13-4
- Fix for CVE-2019-20477
* Tue Apr 16 2019 Tapas Kundu <tkundu@vmware.com> 3.13-3
- Added lib3 changes for CVE-2017-18342
- change default loader for yaml.add_constructor
- Add custom constructors to multiple loaders
* Thu Mar 28 2019 Ankit Jain <ankitja@vmware.com> 3.13-2
- Fix for CVE-2017-18342
* Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 3.13-1
- Updated to release 3.13
* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 3.12-2
- Adding python3 support.
* Tue Apr 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.12-1
- Updated version to 3.12
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11-2
- GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
