Summary:        file locking module
Name:           python3-lockfile
Version:        0.12.2
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/openstack/pylockfile
Source0:        https://pypi.python.org/packages/source/l/lockfile/lockfile-%{version}.tar.gz
%define sha512  lockfile=67b7d651d7e963a497c2604912c61eed90181cdd09c744a0ceaa26e6bbe09d1a871ce48be3949b7da7ea6b366b15492c8c8de589edeca2641ca5e6cb3804df07
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
%autosetup -n lockfile-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%doc ACKS AUTHORS LICENSE PKG-INFO README.rst RELEASE-NOTES doc/
%{python3_sitelib}/lockfile-%{version}-*.egg-info
%{python3_sitelib}/lockfile

%changelog
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.12.2-5
- Update release to compile with python 3.11
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.12.2-4
- Mass removal python2
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.12.2-2
- Fix arch
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.12.2-1
- Initial packaging for Photon
