%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-pywbem
Version:        1.0.1
Release:        1%{?dist}
Summary:        Python WBEM Client
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pywbem.sourceforge.net
Source0:        http://downloads.sourceforge.net/pywbem-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
%define sha1 pywbem=3a079c96ee2fd28cc6a8dbd17f8e6c5c71fcaed3
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
Requires:       python3
Requires:       python3-six
Requires:       python3-xml
Requires:       python3-M2Crypto
Requires:       python3-PyYAML
Requires:       python3-ply

%description
PyWBEM is a Python library for making CIM operations over HTTP using the
WBEM CIM-XML protocol.  WBEM is a manageability protocol, like SNMP,
standardised by the Distributed Management Task Force (DMTF) available
at http://www.dmtf.org/standards/wbem.

%prep
%setup -q -n pywbem-%{version}

%build
CFLAGS="%{optflags}" python3 setup.py build

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
*    Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-    Automatic Version Bump
*    Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.17.4-1
-    Automatic Version Bump
*    Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.15.0-2
-    Mass removal python2
*    Fri Dec 06 2019 Tapas Kundu <tkundu@vmware.com> 0.15.0-1
-    Updated to release 0.15.0
*    Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.12.6-1
-    Updated to release 0.12.6
*    Thu Jul 13 2017 Kumar Kaushik <kaushikk@vmware.com> 0.10.0-1
-    Initial packaging
