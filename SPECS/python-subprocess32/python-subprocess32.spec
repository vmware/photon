Name:           python-subprocess32
Version:        3.2.7
Release:        1%{?dist}
Summary:        A backport of the subprocess module from Python 3.2/3.3 for use on 2.x
License:        PSF
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/subprocess32
Source0:        subprocess32-%{version}.tar.gz
%define sha1    subprocess32=75a8664ba54663016315dae17510af97c5a96953

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
Requires:       python2
Requires:       python2-libs

%description
A backport of the subprocess module from Python 3.2/3.3 for use on 2.x

%prep
%setup -n subprocess32-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.7-1
-   Initial version of python-subprocess32 package for Photon.
