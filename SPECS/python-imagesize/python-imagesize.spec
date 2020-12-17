%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-imagesize
Version:        1.2.0
Release:        2%{?dist}
Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/imagesize_py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/53/72/6c6f1e787d9cab2cc733cf042f125abec07209a58308831c9f292504e826/imagesize-%{version}.tar.gz
%define sha1    imagesize=b88a92cabe93b5a53faacb1cff4e50f8a2d9427a

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-packaging

%if %{with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
python module to analyze jpeg/jpeg2000/png/gif image header and return image size.

%prep
%setup -n imagesize-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
py.test3

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-2
-   Fix build with new rpm
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.1.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-1
-   Update to version 1.1.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-2
-   Change python to python2
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-1
-   Initial
