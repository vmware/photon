%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        file locking module
Name:           python3-lockfile
Version:        0.12.2
Release:        4%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/openstack/pylockfile
Source0:        https://pypi.python.org/packages/source/l/lockfile/lockfile-%{version}.tar.gz
%define sha1    lockfile=c2ac46e48585e5f8f8d57ccc55ca83faa8b53b86
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pbr
Requires:       python3
BuildArch:      noarch

%description
The lockfile package exports a LockFile class which provides a simple API for locking files.
Unlike the Windows msvcrt.locking function, the fcntl.lockf and flock functions, and the
deprecated posixfile module, the API is identical across both Unix (including Linux and Mac)
and Windows platforms. The lock mechanism relies on the atomic nature of the link (on Unix)
and mkdir (on Windows) system calls. An implementation based on SQLite is also provided, more
as a demonstration of the possibilities it provides than as production-quality code.


%prep
%setup -q -n lockfile-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%doc ACKS AUTHORS LICENSE PKG-INFO README.rst RELEASE-NOTES doc/
%{python3_sitelib}/lockfile-%{version}-*.egg-info
%{python3_sitelib}/lockfile

%changelog
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.12.2-4
-   Mass removal python2
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.2-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12.2-2
-   Fix arch
*   Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.12.2-1
-   Initial packaging for Photon
