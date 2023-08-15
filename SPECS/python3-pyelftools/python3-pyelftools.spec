Summary:        Pure-Python library for parsing and analyzing ELF files
Name:           python3-pyelftools
Version:        0.29
Release:        1%{?dist}
License:        Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/eliben/pyelftools
Source0:        https://github.com/eliben/pyelftools/archive/v%{version}/pyelftools-%{version}.tar.gz
%define sha512  pyelftools=0eba3b029a734abe9f8df92cd58bc967f10bf9f61c3a419bdbc5e637200844dddd947bcb485e8ebbe2eeaa7f7e91efc6500316af51aace1db051a658cf61153e

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  llvm-devel
BuildRequires:  binutils

Requires:       python3
Requires:       python3-setuptools
BuildArch:      noarch

%description
Pure-Python library for parsing and analyzing ELF files and DWARF debugging information.

%prep
%autosetup -n pyelftools-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}
pushd %{buildroot}%{_bindir}
mv readelf.py pyreadelf-%{python3_version}
ln -s pyreadelf-%{python3_version} pyreadelf-3
ln -s pyreadelf-3 pyreadelf
popd

%check
%{__python3} test/run_all_unittests.py
%{__python3} test/run_examples_test.py
%{__python3} test/run_readelf_tests.py || :

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/pyreadelf
%{_bindir}/pyreadelf-3*

%changelog
* Mon Aug 14 2023 Susant Sahani <ssahani@vmware.com> 0.29-1
- Introduce on requirement from systemd.
