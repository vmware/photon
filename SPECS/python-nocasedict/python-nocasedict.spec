Name:           python3-nocasedict
Version:        1.0.4
Release:        3%{?dist}
Summary:        A case-insensitive ordered dictionary for Python
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/ad/80/40b0bfddbea87c6e7d400171b42ee1a82b954114d706a8871e0eb4225c60/nocasedict-1.0.2.tar.gz
Source0:        nocasedict-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version}dist(nocasedict)

%description
A case-insensitive ordered dictionary for Python

%prep
%autosetup -n nocasedict-%{version}

%build
%py3_build

%install
%py3_install
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.4-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.4-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
- Initial packaging for python3-nocasedict
