%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python parsing module.
Name:           python3-pyparsing
Version:        2.4.7
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/pyparsing/%{version}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        pyparsing-%{version}.tar.gz
%define sha1    pyparsing=ca8d892c93fe2d54ea5e6f31c5798e40c58e8667

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

%description
Python parsing module.

%prep
%autosetup -p1 -n pyparsing-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%%check
#Tests are not available

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.7-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-4
- Mass removal python2
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.0-3
- Disabled check section as tests are not available
* Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.0-2
- Add build dependency with python-setuptools to handle 1.0 update
* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 2.2.0-1
- Update to 2.2.0 and remove build dependency with python-setuptools
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.10-1
- Initial packaging for Photon
