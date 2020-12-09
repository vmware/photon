%define debug_package %{nil}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        YAML parser/emitter.
Name:           python3-ruamel-yaml
Version:        0.16.12
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/ruamel.yaml
Source0:        https://files.pythonhosted.org/packages/ruamel.yaml-0.16.12.tar.gz
%define sha1    ruamel.yaml=3ab92a0db02457290d9d31b8274c728cf71f81f7
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-typing
%if %{with_check}
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
%setup -q -n ruamel.yaml-%{version}

%build
python3 setup.py build

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
*   Wed Dec 09 2020 Tapas Kundu <tkundu@vmware.com> 0.16.12-1
-   Initial packaging for Photon
