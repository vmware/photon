%define srcname pkgconfig

Name:       python3-pkgconfig
Version:    1.5.5
Release:    3%{?dist}
Summary:    Python interface to the pkg-config command line tool
URL:        https://github.com/matze/pkgconfig
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

# Using github URL but actually downloaded from:
# https://pypi.org/project/pkgconfig/
Source0: https://github.com/matze/pkgconfig/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.5-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.5-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.5-1
- First build. Needed by tpm2-pytss.
