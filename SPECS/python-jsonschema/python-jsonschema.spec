%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-jsonschema
Version:        2.6.0
Release:        2%{?dist}
Summary:        An implementation of JSON Schema validation for Python
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:		http://pypi.python.org/pypi/jsonschema
Source0:        http://pypi.python.org/packages/source/j/jsonschema/jsonschema-%{version}.tar.gz
%define sha1    jsonschema=97e49df4601f7066d9954c0ec4d8d697887b32f0

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-vcversioner

BuildArch:      noarch

%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03


%prep
%setup -n jsonschema-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/jsonschema %{buildroot}/%{_bindir}/jsonschema3

%check
python3 setup test

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/jsonschema3

%changelog
*   Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 2.6.0-2
-   Mass removal python2
*   Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.6.0-1
-   Initial version
