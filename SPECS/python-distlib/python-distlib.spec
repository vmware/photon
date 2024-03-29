%global srcname distlib

Name:           python3-distlib
Version:        0.3.6
Release:        2%{?dist}
Summary:        Low-level components of distutils2/packaging, augmented with higher-level APIs
License:        Python
URL:            https://pypi.org/project/distlib
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/58/07/815476ae605bcc5f95c87a62b95e74a1bce0878bc7a3119bc2bf4178f175/distlib-%{version}.tar.gz
%define sha512 %{srcname}=27f3a59f9175a92befb9a65a66cd0b8eb65185dab6fa13ef94e85ca69c2bc1b7281ce1522601034007cb98677ba9237a46224df4adc70ed966db7e131e073636

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  unzip

Requires:       python3

Provides:       python%{python3_version}dist(distlib)

%description
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%prep
%autosetup -p1 -n %{srcname}-%{version}

rm -rf distlib/*.exe \
       distlib/_backport

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
export PYTHONHASHSEED=0
%{python3} setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.3.6-2
- Spec fixes. Remove readme, license files.
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.3.6-1
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.3.1-1
- initial version
