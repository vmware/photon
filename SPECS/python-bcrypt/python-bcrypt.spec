Name:           python3-bcrypt
Version:        3.2.0
Release:        2%{?dist}
Summary:        Good password hashing for your software and your servers.
License:        Apache License, Version 2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/bcrypt/bcrypt-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        bcrypt-%{version}.tar.gz
%define sha1    bcrypt=3b6246d6e291814441e6ac152b462f8dfc18f5bb

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  python3-pip
%endif

%description
Good password hashing for your software and your servers.


%prep
%autosetup -n bcrypt-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install pytest
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.0-2
-   Update release to compile with python 3.10
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.7-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.1.6-3
-   Mass removal python2
*   Tue Sep 03 2019 Shreyas B. <shreyasb@vmware.com> 3.1.6-2
-   Fix make check errors.
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 3.1.6-1
-   Initial packaging for Photon
