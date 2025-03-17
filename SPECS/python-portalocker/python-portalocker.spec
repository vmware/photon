Summary:        Library to provide an easy API to file locking.
Name:           python3-portalocker
Version:        2.8.2
Release:        2%{?dist}
Url:            https://pypi.org/project/portalocker
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/35/00/0f230921ba852226275762ea3974b87eeca36e941a13cd691ed296d279e5/portalocker-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

Provides: python%{python3_version}dist(portalocker)

%description
Portalocker is a library to provide an easy API to file locking.
On Linux and Unix systems the locks are advisory by default.
By specifying the -o mand option to the mount command it is possible to enable mandatory file locking on Linux

%prep
%autosetup -n portalocker-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
rm pytest.ini
pip3 install redis tomli
%pytest portalocker_tests
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.2-2
- Release bump for SRP compliance
* Tue Jun 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.2-1
- Initial packaging for Photon
