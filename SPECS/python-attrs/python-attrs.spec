%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Attributes without boilerplate.
Name:           python3-attrs
Version:        20.2.0
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/attrs
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        attrs-%{version}.tar.gz
%define sha1    attrs=a87318d8fa3f613b8e7a5f78396c26d628081330

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-zope.interface
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs

%description
Attributes without boilerplate.

%prep
%setup -q -n attrs-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
#python2 does not support for tests
pip3 install pytest hypothesis==4.38.0
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.2.0-2
-   openssl 1.1.1
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 20.2.0-1
-   Automatic Version Bump
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 20.1.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 19.3.0-1
-   Automatic Version Bump
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 18.2.0-4
-   Mass removal python2
*   Thu Feb 27 2020 Tapas Kundu <tkundu@vmware.com> 18.2.0-3
-   hypothesis 4.38.2 has requirement attrs>=19.2.0,
-   but we have attrs 18.2.0 which is incompatible.
*   Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-2
-   Fixed the makecheck errors
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-1
-   Update to version 18.2.0
*   Thu Jul 06 2017 Chang Lee <changlee@vmware.com> 16.3.0-3
-   Updated %check
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-1
-   Initial packaging for Photon
