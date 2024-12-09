Name:           python3-s3transfer
Version:        0.6.0
Release:        3%{?dist}
Summary:        Amazon S3 Transfer Manager for Python
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/66/f5/5ca537483fa5e96fbd455f52a69fc70c5f659f7e8c9189a1dbc211e1ccf9/s3transfer-0.3.7.tar.gz
Source0:        s3transfer-%{version}.tar.gz
%define sha512  s3transfer=0c1c3306015cab4a4436b1d2fec6708e17f4c5111f8a265fbfe134defebda33a43bd985e559be993b6175af9eee142e9f27da123f8d14f77cfc59e48ca1b905f

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
Requires:       python3-botocore
BuildArch:      noarch
Provides:       python%{python3_version}dist(s3transfer)

%description
A transfer manager for Amazon Web Services S3

%prep
%autosetup -n s3transfer-%{version}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.6.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.6.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.6.0-1
- Automatic Version Bump
* Tue Jul 20 2021 Tapas Kundu <tkundu@vmware.com> 0.3.7-1
- Initial packaging for python3-s3transfer
