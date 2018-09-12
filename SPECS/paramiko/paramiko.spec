%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python SSH module
Name:           paramiko
Version:        2.4.1
Release:        1%{?dist}
License:        LGPL
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.paramiko.org/
Source0:        https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define         sha1 paramiko=387453007741531d65e8072696049418c57e4162

BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  ecdsa > 0.11
BuildRequires:  pycrypto > 2.1
BuildRequires:  python-cryptography

Requires:       python2
Requires:       pycrypto > 2.1
Requires:       ecdsa > 0.11
Requires:       python-cryptography


%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%package -n     python3-paramiko
Summary:        python3-paramiko
BuildRequires:  python3-devel
BuildRequires:  python3-ecdsa > 0.11
BuildRequires:  python3-pycrypto > 2.1
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-pycrypto > 2.1
Requires:       python3-ecdsa > 0.11
Requires:       python3-cryptography
%description -n python3-paramiko

Python 3 version.

%prep
%setup -q

%build
python2 setup.py build
python3 setup.py build

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
LANG=en_US.UTF-8 python2 test.py
LANG=en_US.UTF-8 python3 test.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc *.txt
%{python2_sitelib}/*

%files -n python3-paramiko
%defattr(-, root, root)
%doc *.txt
%{python3_sitelib}/*

%changelog
*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.1-1
-   Update version to 2.4.1
*   Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 2.1.5-1
-   Update version to 2.1.5 for CVE-2018-1000132
*   Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-5
-   Fixed test command
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-3
-   Use python2 explicitly while building
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
-   Added missing requires python-cryptography
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-1
-   Update to 2.1.2
*   Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-4
-   Added python3 site-packages.
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.16.0-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16.0-2
-   GA - Bump release of all rpms
*   Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-1
-   Initial build.  First version
