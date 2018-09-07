%define sha1    markupsafe=aed40fbcf0423f3ea005892a2e7144e44ff81745
%define sha1    markupsafe=aed40fbcf0423f3ea005892a2e7144e44ff81745

Summary:        A XML/HTML/XHTML Markup safe string for Python.
Name:           python-markupsafe
Version:        1.0
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/MarkupSafe
Source0:        https://pypi.python.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-%{version}.tar.gz 
%define sha1    markupsafe=aed40fbcf0423f3ea005892a2e7144e44ff81745

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%package -n     python3-markupsafe
Summary:        python-markupsafe
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-markupsafe
Python 3 version.

%prep
%setup -q -n MarkupSafe-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-markupsafe
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Sep 07 2018 Tapas Kundu <tkundu@vmware.com> 1.0-1
-   Update to version 1.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0-2
-   Removed erroneous version line
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.0-1
-   Upgrade version to 1.0
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.23-1
-   Initial packaging for Photon
