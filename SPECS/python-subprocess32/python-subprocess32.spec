%define python2_ver %(python2 -c "import sys;print sys.version[0:3]")

Name:           python-subprocess32
Version:        3.2.7
Release:        1%{?dist}
Summary:        A backport of the subprocess module from Python 3.2/3.3 for use on 2.x
License:        PSF
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/subprocess32
Source0:        subprocess32-%{version}.tar.gz
%define sha1    subprocess32=75a8664ba54663016315dae17510af97c5a96953
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
%if %{with_check}
BuildRequires:  python2-test
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools

%description
A backport of the subprocess module from Python 3.2/3.3 for use on 2.x

%prep
%setup -n subprocess32-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PYTHONPATH=build/lib.linux-%{_arch}-%{python2_ver}/ python2 test_subprocess32.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Fri Oct 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.7-1
-   Initial version of python-subprocess32 package for Photon.
