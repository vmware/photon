Name:           python3-pluggy
Version:        0.13.1
Release:        2%{?dist}
Summary:        The plugin manager stripped of pytest specific details
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.org/project/pluggy/
Source0:        https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-%{version}.tar.gz
%define sha1    pluggy=828b2c10996d902b8c47f2fded0e101c636b9ff9
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
Requires:       python3

Provides:       python3dist(pluggy) = %{version}-%{release}
Provides:       python%{python3_version}dist(pluggy) = %{version}-%{release}

%description
The plugin manager stripped of pytest specific details.

%prep
%autosetup -p1 -n pluggy-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.13.1-2
- Update release to compile with python 3.10
* Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com> 0.13.1-1
- Initial rpm release
