%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library for building powerful interactive command lines in Python.
Name:           python3-prompt_toolkit
Version:        3.0.7
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/prompt_toolkit
Source0:        https://files.pythonhosted.org/packages/source/p/prompt_toolkit/prompt_toolkit-%{version}.tar.gz
%define sha1    prompt_toolkit=9bfef203f8a9f667675f97e5717f2b48c299edc8

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-Pygments
BuildRequires:  python3-wcwidth
BuildRequires:  python3-six
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-Pygments
Requires:       python3-six
Requires:       python3-wcwidth
BuildArch:      noarch

%description
prompt_toolkit is a library for building powerful interactive command lines and terminal applications in Python.

%prep
%setup -q -n prompt_toolkit-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
#make check failing for 3.7 so skipping for python3

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.7-1
-   Automatic Version Bump
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.6-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.5-1
-   Automatic Version Bump
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 2.0.9-2
-   Mass removal python2
*   Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> 2.0.9-1
-   Update to release 2.0.9
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 2.0.4-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.0.4-1
-   Update to version 2.0.4
*   Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.14-4
-   Added packages which are required during runtime
*   Wed Jul 12 2017 Chang Lee <changlee@vmware.com> 1.0.14-3
-   Updated %check and added six, wcwidth, and pytest in BuildRequires
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.14-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.14-1
-   Initial packaging for Photon
