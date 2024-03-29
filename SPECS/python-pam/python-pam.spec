Summary:        Python PAM module using ctypes, py3/py2
Name:           python3-pam
Version:        2.0.2
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/python-pam/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        python-pam-%{version}.tar.gz
%define sha512  python-pam=a33279d47de07b32c5c5cadb0f666ea18b407de061cb80e0b1d6cd7370fd70ff14af8d2802a2e4dbdaaf102efd6cac83c4f2c5673615b3d174edca20a4f8b00a

BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description
Python PAM module using ctypes, py3/py2.

%prep
%autosetup -n python-pam-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Thu Feb 18 2021 Tapas Kundu <tkundu@vmware.com> 1.8.4-1
- Initial packaging for Photon
