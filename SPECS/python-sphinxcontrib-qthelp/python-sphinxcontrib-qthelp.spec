%define srcname sphinxcontrib-qthelp

Name:           python3-sphinxcontrib-qthelp
Version:        1.0.3
Release:        3%{?dist}
Summary:        Sphinx extension for QtHelp documents
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-qthelp
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/b1/8e/c4846e59f38a5f2b4a0e3b27af38f2fcf904d4bfd82095bf92de0b114ebd/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=29f77e4b3f1a4868c2a34dbd853415e5d813f482cd23b982aeed42d53acba09b896d77ba930c34cce8af043bb7d64a19acff610430e942038d95a410b6e0b5fa

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp document.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-3
- Fix summary & description
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.3-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.3-1
- initial version
