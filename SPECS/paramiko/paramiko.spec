Summary: Python SSH module
Name: paramiko
Version: 1.16.0
Release: 1%{?dist}
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
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%prep
%setup -q

%build
easy_install ./

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc *.txt
%{python_sitelib}/*

%changelog
*	Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-1
-	Initial build.	First version