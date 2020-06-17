# Got the intial spec and patches from Fedora and modified the spec.
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python bindings for PAM (Pluggable Authentication Modules).
Name:           python3-PyPAM
Version:        0.5.0
Release:        5%{?dist}
License:        LGPLv2
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
# Note that the upstream site is dead.
Source0:        http://www.pangalactic.org/PyPAM/PyPAM-%{version}.tar.gz
Url:            http://www.pangalactic.org/PyPAM
%define sha1    PyPAM=fac6c2958fffc38454b1104d2d0f1f28563eff42
Patch0:         PyPAM-dlopen.patch
Patch1:         PyPAM-0.5.0-dealloc.patch
Patch2:         PyPAM-0.5.0-nofree.patch
Patch3:         PyPAM-0.5.0-memory-errors.patch
Patch4:         PyPAM-0.5.0-return-value.patch
Patch5:         PyPAM-python3-support.patch

BuildRequires:  python3-setuptools
BuildRequires:  Linux-PAM-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description
Python bindings for PAM (Pluggable Authentication Modules).


%prep
%setup -q -n PyPAM-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 tests/PamTest.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 0.5.0-5
-   Mass removal python2
*   Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 0.5.0-4
-   Added BuildRequires python2-devel.
-   Moved all buildRequires to the main package.
*   Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-3
-   Fix the check section
*   Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-2
-   Changing python_sitelib to python2
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
-   Initial packaging for Photon.
