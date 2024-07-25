Name:           python3-pluggy
Version:        1.0.0
Release:        1%{?dist}
Summary:        The plugin manager stripped of pytest specific details
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.org/project/pluggy/
Source0:        https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-%{version}.tar.gz
%define sha512  pluggy=cf0bcbb4330c24ce473614befa19548f33fb39fa0ad094e1eae786202d7adadc28e16499f80ab96b630091765404ca5c5b6f9a55bc605e03514d8ab50cf9ae00
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
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
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
- Automatic Version Bump
* Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com> 0.13.1-1
- Initial rpm release
