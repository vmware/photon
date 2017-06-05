%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Service identity verification for pyOpenSSL.
Name:           python-service_identity
Version:        16.0.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity
Source0:        service_identity-%{version}.tar.gz
%define         sha1 service_identity=42617f5abbd917c663aea58c4628b82e80d245ce

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
service_identity aspires to give you all the tools you need for verifying whether a certificate is valid for the intended purposes.

In the simplest case, this means host name verification. However, service_identity implements RFC 6125 fully and plans to add other relevant RFCs too.

%package -n     python3-service_identity
Summary:        python-service_identity
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs
%description -n python3-service_identity
Python 3 version.

%prep
%setup -q -n service_identity-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-service_identity
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.0.0-1
-   Initial packaging for Photon.
