%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-nocasedict
Version:        1.0.2
Release:        1%{?dist}
Summary:        A case-insensitive ordered dictionary for Python
License:        GNU Lesser General Public License v2 or later (LGPLv2+)
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/ad/80/40b0bfddbea87c6e7d400171b42ee1a82b954114d706a8871e0eb4225c60/nocasedict-1.0.2.tar.gz
Source0:        nocasedict-%{version}.tar.gz
%define sha1    nocasedict=a4b8bc6d926f0588e19c9150faa5bfb1e95aad41
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python3.9dist(nocasedict)

%description
A case-insensitive ordered dictionary for Python

%prep
%autosetup -n nocasedict-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.0.2-1
-   Initial packaging for python3-nocasedict
