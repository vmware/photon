Summary:        Measures number of Terminal column cells of wide-character codes.
Name:           python3-wcwidth
Version:        0.2.5
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/wcwidth
Source0:        https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-%{version}.tar.gz
%define         sha512 wcwidth=567604186fc6810cc794828f656aebda380a85d9a0dadde7743fadcd43cf29b022016055ee2a5c077399ac7c07f48d6d4ee4fa91a44e6efed96b7a8659280a97

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

%prep
%autosetup -p1 -n wcwidth-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.5-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.5-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.1.7-3
- Mass removal python2
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.7-1
- Initial packaging for Photon
