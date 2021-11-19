Name:           python3-more-itertools
Version:        8.5.0
Release:        2%{?dist}
Summary:        More routines for operating on Python iterables, beyond itertools
Group:          Development/Libraries
License:        MIT
URL:            https://github.com/erikrose/more-itertools
Source0:        https://files.pythonhosted.org/packages/d6/03/37d7c431c4c1c17507fb7b89240ddb7be70f2027277960d525f1679363c1/more-itertools-%{version}.tar.gz
%define sha1    more-itertools=2ec6794a07339fb06d6545d03945cf3702c4ee2a
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
Requires:       python3

Provides:       python3dist(more-itertools) = %{version}-%{release}
Provides:       python%{python3_version}dist(more-itertools) = %{version}-%{release}

%description
Python's itertools library is a gem - you can compose elegant solutions for
a variety of problems with the functions it provides. In more-itertools we
collect additional building blocks, recipes, and routines for working with
Python iterables

%prep
%autosetup -n more-itertools-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 8.5.0-2
-   Update release to compile with python 3.10
*   Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com> 8.5.0-1
-   Initial rpm release
