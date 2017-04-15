%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python SSH module
Name:           paramiko
Version:        2.1.2
Release:        1%{?dist}
License:        LGPL
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.paramiko.org/
Source0:        https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define         sha1 paramiko=8802efc2f4b23f83c677885d9210e359fc20133c

BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  ecdsa > 0.11
BuildRequires:  pycrypto > 2.1

Requires:       python2
Requires:       pycrypto > 2.1
Requires:       ecdsa > 0.11


%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%package -n     python3-paramiko
Summary:        python3-paramiko
BuildRequires:  python3-devel
BuildRequires:  python3-ecdsa > 0.11
BuildRequires:  python3-pycrypto > 2.1

Requires:       python3
Requires:       python3-pycrypto > 2.1
Requires:       python3-ecdsa > 0.11
%description -n python3-paramiko

Python 3 version.

%prep
%setup -q

%build
python setup.py build
python3 setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
%{__python}  test.py
python3   test.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc *.txt
%{python_sitelib}/*

%files -n python3-paramiko
%defattr(-, root, root)
%doc *.txt
%{python3_sitelib}/*

%changelog
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
