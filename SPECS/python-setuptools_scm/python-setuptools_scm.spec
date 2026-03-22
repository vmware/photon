%global build_if %{photon_subrelease} >= 92

Summary:        the blessed package to manage your versions by scm tags.
Name:           python3-setuptools_scm
Version:        9.2.2
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch

%description
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%prep
%autosetup -p1 -n setuptools_scm-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/setuptools-scm
%{python3_sitelib}/*

%changelog
* Tue Dec 09 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 9.2.2-1
- Upgrade to 9.2.2 as part of python3 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.0.5-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.5-1
- Automatic Version Bump
* Thu Sep 03 2020 Tapas Kundu <tkundu@vmware.com> 4.1.2-2
- Requires python3-setuptools for installation
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.1.2-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.1.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.1.0-1
- Update to version 3.1.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
- Initial packaging for Photon
