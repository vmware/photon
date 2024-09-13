Name:           python3-jsonschema
Version:        3.2.0
Release:        3%{?dist}
Summary:        An implementation of JSON Schema validation for Python
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://pypi.python.org/pypi/jsonschema
Source0:        http://pypi.python.org/packages/source/j/jsonschema/jsonschema-%{version}.tar.gz
%define sha512  jsonschema=acbb4cec730a8cdab9f070593ed896064fbe082d464ec362adc952e4985e9eaa12ad0f2d55a04018ffdaf675e54037999a7219533dad6b84bf609f5dfe21bbab

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-vcversioner
BuildRequires:  python3-setuptools_scm
Requires:       python3-pyrsistent
Requires:       python3-attrs
BuildArch:      noarch

%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%prep
%autosetup -n jsonschema-%{version}

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
* Fri Sep 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 3.2.0-3
- Bump-up to compile with python3-attrs-22.2.0
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.0-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 2.6.0-2
- Mass removal python2
* Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.6.0-1
- Initial version
