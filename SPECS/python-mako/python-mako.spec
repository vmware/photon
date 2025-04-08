Name:           python3-mako
Version:        1.2.4
Release:        1%{?dist}
Summary:        Python templating language
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://www.makotemplates.org
Source0: https://github.com/sqlalchemy/mako/archive/refs/tags/Mako-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
A super-fast templating language that borrows the best ideas from the existing templating languages. Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles into Python modules for maximum performance. Mako’s syntax and API borrows from the best ideas of many others, including Django templates, Cheetah, Myghty, and Genshi.

%prep
%autosetup -p1 -n mako-rel_1_2_4

%build
%py3_build

%install
%py3_install
mv %{buildroot}%{_bindir}/mako-render %{buildroot}%{_bindir}/mako-render3

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/mako-render3

%changelog
* Tue Apr 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.4-1
- Upgrade to fix CVE-2022-40023
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.2.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.3-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.3-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.0.7-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.0.7-1
- Update to version 1.0.7
* Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-5
- Fix make check issues.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.6-3
- Separate the python2 and python3 specific scripts in the bin directory
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.6-2
- Added python3 package.
* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.6-1
- Initial version of python-mako package for Photon.
