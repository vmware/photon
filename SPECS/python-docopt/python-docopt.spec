Name:           python3-docopt
Version:        0.6.2
Release:        5%{?dist}
Summary:        Pythonic argument parser to create command line interfaces.
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/docopt
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: docopt-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
docopt helps easily create most beautiful command-line interfaces.

%prep
%autosetup -p1 -n docopt-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.6.2-5
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.6.2-4
- Update release to compile with python 3.11
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.6.2-3
- Fix build with new rpm
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.6.2-2
- Mass removal python2
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.2-1
- Initial version of python-docopt package for Photon.
