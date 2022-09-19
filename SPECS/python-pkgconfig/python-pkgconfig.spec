%define srcname pkgconfig

Name:       python3-pkgconfig
Version:    1.5.5
Release:    2%{?dist}
Summary:    Python interface to the pkg-config command line tool
License:    MIT
URL:        https://github.com/matze/pkgconfig
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

# Using github URL but actually downloaded from:
# https://pypi.org/project/pkgconfig/
Source0: https://github.com/matze/pkgconfig/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=ffa838d0146125c4158b747b619cc5eed41da0e2f04664a4db89909a486922120a0e1779f99dfcda0da3e98b8770c57b638a9c7bc5994cd8102aa3cf990905b0

BuildRequires: python3-devel
BuildRequires: python3-setuptools

BuildArch:      noarch

%description
pkgconfig is a Python module to interface with the pkg-config command line
tool and supports Python 2.6+.

It can be used to
* check if a package exists
* check if a package meets certain version requirements
* query CFLAGS and LDFLAGS
* parse the output to build extensions with setup.py

If pkg-config is not on the path, raises EnvironmentError.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.5-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.5-1
- First build. Needed by tpm2-pytss.
