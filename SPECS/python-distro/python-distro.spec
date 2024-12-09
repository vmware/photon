%define debug_package %{nil}

Summary:        Distro - an OS platform information API
Name:           python3-distro
Version:        1.7.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/distro
Source0:        https://files.pythonhosted.org/packages/ca/e3/78443d739d7efeea86cbbe0216511d29b2f5ca8dbf51a6f2898432738987/distro-%{version}.tar.gz
%define sha512  distro=14516ecab33ee8c57c35a8279eb515fd699031fabac7d8886092ea98696797d55503179870aeb513a85e1a66c7e69f2f60bb6ea9fc935be975cb5135e1917ecc

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif
Requires:       photon-release
Requires:       python3
BuildArch:      noarch
%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%prep
%autosetup -n distro-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
pip3 install tox
tox

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
/usr/bin/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.7.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.0-1
- Automatic Version Bump
* Wed Jul 24 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-3
- Obsolete python-distro
* Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-2
- Separate spec file for python3-distro package in Photon
