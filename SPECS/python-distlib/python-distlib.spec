%global srcname distlib

Name:       python3-distlib
Version:    0.3.1
Release:    1%{?dist}
Summary:    Low-level components of distutils2/packaging, augmented with higher-level APIs
License:    Python
URL:        https://pypi.org/project/distlib/
Source0:    https://files.pythonhosted.org/packages/2f/83/1eba07997b8ba58d92b3e51445d5bf36f9fba9cb8166bcae99b9c3464841/distlib-%{version}.zip
%define sha1    distlib=1c575431e31c32d25596c360e81bba7fe4638669
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Patch0: distlib_unbundle.patch

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  unzip

Requires:       python3

Provides:       python3.9dist(distlib) = %{version}-%{release}

%description
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

rm distlib/*.exe
rm -rf distlib/_backport
rm tests/test_shutil.py*
rm tests/test_sysconfig.py*

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%if %{with check}
%check
export PYTHONHASHSEED=0
%{python3} setup.py test
%endif # with_tests

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc README.rst
%license LICENSE.txt

%changelog
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.3.1-1
- initial version
