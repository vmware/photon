Summary:        A XML/HTML/XHTML Markup safe string for Python.
Name:           python3-markupsafe
Version:        2.1.1
Release:        4%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/pallets/markupsafe

Source0: https://github.com/pallets/markupsafe/archive/refs/tags/markupsafe-%{version}.tar.gz
%define sha512 markupsafe=6b06a5f470858409eb186d20edd129be90f31030be91fcc73e989b0a4ee51c3755cce0938edd9a7c73471d307385260f868101b5e11cc4d97c309420b5a573da

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%prep
%autosetup -p1 -n markupsafe-%{version}

%build
%py3_build

%install
%py3_install
rm %{buildroot}%{python3_sitearch}/markupsafe/*.c

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.1.1-4
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.1-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.1.1-2
- Update release to compile with python 3.11
* Mon Sep 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.1.1-1
- Upgrade to 2.1.1, required for python3-jinja2
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 1.1.1-1
- Update to 1.1.1
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.0-4
- Mass removal python2
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0-2
- Removed erroneous version line
* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.0-1
- Upgrade version to 1.0
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.23-1
- Initial packaging for Photon
