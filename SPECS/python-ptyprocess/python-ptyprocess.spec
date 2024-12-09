Summary:        Run a subprocess in a pseudo terminal.
Name:           python3-ptyprocess
Version:        0.7.0
Release:        3%{?dist}
Url:            https://github.com/pexpect/ptyprocess
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/ptyprocess/ptyprocess-%{version}.tar.gz
%define sha512  ptyprocess=791d8f2e79900627215ce80ce67ee9c79173dbc08297c6219d5058f9b80c5e323b93049e6836a70c4073f43548d22e3cf310f2e9948ef12f96bcaa15b0ddb2f3

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-xml
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.

%prep
%autosetup -n ptyprocess-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pathlib2 funcsigs pluggy more_itertools
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.7.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.6.0-6
- openssl 1.1.1
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.6.0-5
- Mass removal python2
* Wed Feb 26 2020 Tapas Kundu <tkundu@vmware.com> 0.6.0-4
- Fix make check
* Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 0.6.0-3
- Fix make check
* Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 0.6.0-2
- Add %check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.6.0-1
- Update to version 0.6.0
* Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 0.5.2-1
- Initial packaging for Photon
