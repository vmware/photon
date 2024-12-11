Summary:        provides a pure-Python implementation of immutable URLs
Name:           python3-hyperlink
Version:        21.0.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/python-hyper/hyperlink
Source0:        https://github.com/python-hyper/hyperlink/archive/hyperlink-%{version}.tar.gz
%define sha512  hyperlink=9e0e9273dde1b0a41329a74fbb26c4f327b87f387ee64b9a2ab641ca5cc8b9ea0516884415e9adf1d4880ae9c053a5cba2c550fc508bb56fddb44a543d5da860

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%if 0%{?with_check}
BuildRequires:  python3-idna
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
BuildArch:      noarch

%description
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%prep
%autosetup -n hyperlink-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
pytest

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.0.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 21.0.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.0.1-2
- openssl 1.1.1
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 19.0.0-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 18.0.0-3
- Mass removal python2
* Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
- Fix make check.
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
- Update to version 18.0.0
* Wed Sep 20 2017 Bo Gan <ganb@vmware.com> 17.3.1-2
- Fix make check issues
* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.3.1-1
- Initial packaging for Photon
