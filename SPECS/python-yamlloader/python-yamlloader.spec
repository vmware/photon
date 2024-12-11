Name:           python3-yamlloader
Version:        1.1.0
Release:        3%{?dist}
Summary:        Ordered YAML loader and dumper for PyYAML.
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/9e/10/fbb1fb0d600f167b4ddeb83a5e66307c5c0d56860595e02c9387861b686d/yamlloader-1.1.0.tar.gz
Source0:        yamlloader-%{version}.tar.gz
%define sha512  yamlloader=dfd85de2a3488f312edbe1ebe3594612d76034221fe1e06ee036229060ddccb8a36b83ca46f0adca58e4581c345f2c57dac2bbdebb59b0fd9bc13ce80162ce46

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version}dist(yamlloader)

%description
This module provides loaders and dumpers for PyYAML. Currently, an OrderedDict loader/dumper is implemented, allowing to keep items order when loading resp. dumping a file from/to an OrderedDict (Python 3.7+: Also regular dicts are supported and are the default items to be loaded to. As of Python 3.7 preservation of insertion order is a language feature of regular dicts.)

%prep
%autosetup -n yamlloader-%{version}

%build
%py3_build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.0-2
- Update release to compile with python 3.11
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.1.0-1
- Initial packaging for python3-yamlloader
