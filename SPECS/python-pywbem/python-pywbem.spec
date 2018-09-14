%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-pywbem
Version:        0.12.6
Release:        1%{?dist}
Summary:        Python WBEM Client
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pywbem.sourceforge.net
Source0:        http://downloads.sourceforge.net/pywbem-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
%define sha1 pywbem=0a75b4c5ca8303351b3942901dbd314cf4120157
BuildRequires:  python2-devel
BuildRequires:  python-pip
BuildRequires:  python-xml
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
Requires:       python2
Requires:       python-six
Requires:       python-xml
Requires:       python-M2Crypto
Requires:       PyYAML
Requires:       python-ply

%description
PyWBEM is a Python library for making CIM operations over HTTP using the 
WBEM CIM-XML protocol.  WBEM is a manageability protocol, like SNMP,
standardised by the Distributed Management Task Force (DMTF) available
at http://www.dmtf.org/standards/wbem.


%package -n     python3-pywbem
Summary:        python3 version of python WBEM client.
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

%description -n python3-pywbem
Python 3 version.

%post -n python3-pywbem
if [ $1 -eq 1 ];then
    # This is initial installation
    ln -s %{python3_sitelib}/pywbem/mof_compiler /usr/bin/mofcomp3
    ln -s %{python3_sitelib}/pywbem/wbemcli /usr/bin/pywbemcli3
fi

%postun -n python3-pywbem
if [ $1 -eq 0 ];then
    # This is erase operation
    rm -f /usr/bin/mofcomp3
    rm -f /usr/bin/pywbemcli3
fi

%prep
%setup -q -n pywbem-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="%{optflags}" python2 setup.py build
pushd ../p3dir
CFLAGS="%{optflags}" python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install -O1 --prefix=%{_prefix} --skip-build --root=%{buildroot}
mv %{buildroot}%{_bindir}/* %{buildroot}%{python2_sitelib}/pywbem/
chmod +x %{buildroot}%{python2_sitelib}/pywbem/wbemcli.py
chmod +x %{buildroot}%{python2_sitelib}/pywbem/mof_compiler.py
install -d %{buildroot}/usr/bin

pushd ../p3dir

python3 setup.py install -O1 --prefix=%{_prefix} --skip-build --root=%{buildroot}
mv %{buildroot}%{_bindir}/* %{buildroot}%{python3_sitelib}/pywbem/
chmod +x %{buildroot}%{python3_sitelib}/pywbem/wbemcli.py
chmod +x %{buildroot}%{python3_sitelib}/pywbem/mof_compiler.py

popd

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ];then
    # This is initial installation
    ln -s %{python2_sitelib}/pywbem/mof_compiler /usr/bin/mofcomp2
    ln -s %{python2_sitelib}/pywbem/wbemcli /usr/bin/pywbemcli2
fi

%postun
if [ $1 -eq 0 ];then
    # This is erase operation
    rm -f /usr/bin/mofcomp2
    rm -f /usr/bin/pywbemcli2
fi

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-pywbem
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*    Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.12.6-1
-    Updated to release 0.12.6
*    Thu Jul 13 2017 Kumar Kaushik <kaushikk@vmware.com> 0.10.0-1
-    Initial packaging
