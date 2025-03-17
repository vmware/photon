Name:           python3-jsonschema
Version:        4.16.0
Release:        2%{?dist}
Summary:        An implementation of JSON Schema validation for Python
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://python-jsonschema.readthedocs.io/en/stable

Source0: https://github.com/python-jsonschema/jsonschema/archive/refs/tags/jsonschema-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pathspec
BuildRequires:  python3-hatch-fancy-pypi-readme
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-hatchling
BuildRequires:  python3-pluggy
BuildRequires:  python3-packaging
BuildRequires:  python3-vcversioner
BuildRequires:  python3-setuptools_scm

Requires:       python3
Requires:       python3-pyrsistent
Requires:       python3-attrs

BuildArch:      noarch

%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%prep
%autosetup -p1 -n jsonschema-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}
mv %{buildroot}/%{_bindir}/jsonschema %{buildroot}/%{_bindir}/jsonschema3

%check
python3 setup test

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/jsonschema3

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 4.16.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.16.0-1
- Update to 4.16.0
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 2.6.0-2
- Mass removal python2
* Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.6.0-1
- Initial version
