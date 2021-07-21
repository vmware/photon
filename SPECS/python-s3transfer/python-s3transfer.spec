%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-s3transfer
Version:        0.3.7
Release:        1%{?dist}
Summary:        Amazon S3 Transfer Manager for Python
License:        Apache-2.0 License
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/66/f5/5ca537483fa5e96fbd455f52a69fc70c5f659f7e8c9189a1dbc211e1ccf9/s3transfer-0.3.7.tar.gz
Source0:        s3transfer-%{version}.tar.gz
%define sha1    s3transfer=816f3e07c70d0dfb71669eba7d29539b003dd01a
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
Requires:       python3-botocore
BuildArch:      noarch

%description
A transfer manager for Amazon Web Services S3

%prep
%autosetup -n s3transfer-%{version}

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
*   Tue Jul 20 2021 Tapas Kundu <tkundu@vmware.com> 0.3.7-1
-   Initial packaging for python3-s3transfer
