Name:           python3-pywbem
Version:        1.4.1
Release:        3%{?dist}
Summary:        Python WBEM Client
Group:          Development/Libraries
URL:            http://pywbem.sourceforge.net
Source0:        http://downloads.sourceforge.net/pywbem-%{version}.tar.gz
%define sha512 pywbem=a39a2200ec9c831b5d21768d91cab7f16e8d4b351881c27bdcf195ac3704b1ebea0355c259a7c9a9ba055999df50025a03d787a1033130de764d183af512c3c8

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-wheel
Requires:       python3
Requires:       python3-six
Requires:       python3-xml
Requires:       python3-M2Crypto
Requires:       python3-PyYAML
Requires:       python3-ply
Requires:       python3-mock
Requires:       python3-nocasedict
Requires:       python3-nocaselist
Requires:       python3-requests
Requires:       python3-yamlloader

Provides:       python%{python3_version}dist(pywbem)

%description
PyWBEM is a Python library for making CIM operations over HTTP using the
WBEM CIM-XML protocol.  WBEM is a manageability protocol, like SNMP,
standardised by the Distributed Management Task Force (DMTF) available
at http://www.dmtf.org/standards/wbem.

%prep
%autosetup -n pywbem-%{version}

%build
CFLAGS="%{optflags}" %py3_build

%install
rm -rf %{buildroot}
python3 setup.py install -O1 --prefix=%{_prefix} --skip-build --root=%{buildroot}
mv %{buildroot}%{_bindir}/* %{buildroot}%{python3_sitelib}/pywbem/

%post
if [ $1 -eq 1 ];then
    # This is initial installation
    ln -s %{python3_sitelib}/pywbem/mof_compiler /usr/bin/mofcomp3
    ln -s %{python3_sitelib}/pywbem/wbemcli /usr/bin/pywbemcli3
fi

%postun
if [ $1 -eq 0 ];then
    # This is erase operation
    rm -f /usr/bin/mofcomp3
    rm -f /usr/bin/pywbemcli3
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.1-3
- Release bump for SRP compliance
* Tue Jun 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.1-2
- Add python3-requests to Requires
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu2vmware.com> 1.1.2-2
- Fix the install issue
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.2-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.17.4-1
- Automatic Version Bump
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.15.0-2
- Mass removal python2
* Fri Dec 06 2019 Tapas Kundu <tkundu@vmware.com> 0.15.0-1
- Updated to release 0.15.0
* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.12.6-1
- Updated to release 0.12.6
* Thu Jul 13 2017 Kumar Kaushik <kaushikk@vmware.com> 0.10.0-1
- Initial packaging
