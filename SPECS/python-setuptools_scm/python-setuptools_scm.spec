Summary:        the blessed package to manage your versions by scm tags.
Name:           python3-setuptools_scm
Version:        7.0.5
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz
%define sha512  setuptools_scm=5b3420f0aaa0dd1655afb0fdcedc3738b75dbb9d8205e0ad67555c251d330a0d3620a7297cfdcfabbc7386a8acf43fe73fa7f3b17e2d156495fd8b2ab7d1c985

Patch0:         build_with_py311.patch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools

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
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.0.5-1
-   Automatic Version Bump
*   Thu Sep 03 2020 Tapas Kundu <tkundu@vmware.com> 4.1.2-2
-   Requires python3-setuptools for installation
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.1.2-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.1.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.1.0-1
-   Update to version 3.1.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
-   Initial packaging for Photon
