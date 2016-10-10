Summary: Python SSH module
Name: paramiko
Version: 1.16.0
Release: 3%{?dist}
License: LGPL
Group: System Environment/Security
URL: http://www.paramiko.org/

Source0: https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define sha1 paramiko=adf3afcc9e5a3f299a20639771f587a803924443

BuildArch: noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  ecdsa > 0.11
BuildRequires: pycrypto > 2.1

Requires: python2
Requires: pycrypto > 2.1
Requires: ecdsa > 0.11


%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%prep
%setup -q

%build
easy_install ./

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
python test.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc *.txt
%{python_sitelib}/*

%changelog
*       Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.16.0-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16.0-2
-	GA - Bump release of all rpms
*	Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-1
-	Initial build.	First version
