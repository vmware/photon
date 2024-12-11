%define debug_package %{nil}

Summary:        YAML parser/emitter.
Name:           python3-ruamel-yaml
Version:        0.17.21
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/ruamel.yaml
Source0:        https://files.pythonhosted.org/packages/ruamel.yaml-%{version}.tar.gz
%define sha512  ruamel.yaml=1ecda5ecacf913a499e40b4df8d5d6112b8c2facf5ce42c36eedad1ea4745884f98919b70a9d51ba8b095463e27371f6b84e314fe8f512c318963ab32f2cbf17

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-typing
%if 0%{?with_check}
BuildRequires:  python3-attrs
BuildRequires:  python3-six
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-xml
Requires:       python3-setuptools
Requires:       python3-typing

%description
ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order

%prep
%autosetup -n ruamel.yaml-%{version}

%build
%py3_build

%install
python3 setup.py install --single-version-externally-managed --skip-build --root=%{buildroot}
find %{buildroot} -name '*.pyc' -delete

%check
#Right now we do not have test in the tar source.
#keeping this code to add the test source and run makecheck
#pip3 install pluggy
#pip3 install more-itertools
#pytest3 _test/test_*.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.21-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.17.21-1
- Automatic Version Bump
* Wed Dec 09 2020 Tapas Kundu <tkundu@vmware.com> 0.16.12-1
- Initial packaging for Photon
