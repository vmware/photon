%global srcname distlib

Name:       python3-distlib
Version:    0.3.1
Release:    3%{?dist}
Summary:    Low-level components of distutils2/packaging, augmented with higher-level APIs
License:    Python
URL:        https://pypi.org/project/distlib
Group:      Development/Languages/Python
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/2f/83/1eba07997b8ba58d92b3e51445d5bf36f9fba9cb8166bcae99b9c3464841/distlib-%{version}.zip
%define sha512 %{srcname}=4c004b09eb93a6bfdd8b9b58175b756aa376c45fdef43a362a52fbffa19feef4850f0eb0f958bbf1eb9d2b8bfc1fc8a67c5b926d954e934c777b5c8b5c18e9d4

Patch0: distlib_unbundle.patch

BuildArch:  noarch

BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  unzip

Requires:       python3

Provides:       python%{python3_version}dist(distlib) = %{version}-%{release}

%description
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%prep
%autosetup -p1 -n %{srcname}-%{version}

rm -rf distlib/*.exe \
       distlib/_backport \
       tests/test_shutil.py* \
       tests/test_sysconfig.py*

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONHASHSEED=0
%{python3} setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Mar 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.3.1-3
- Fix spec issues and remove readme & license files.
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.3.1-2
- Update release to compile with python 3.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.3.1-1
- initial version
