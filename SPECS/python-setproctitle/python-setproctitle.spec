%global tarname setproctitle

Name:           python-setproctitle
Version:        1.3.2
Release:        1%{?dist}
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
Summary:        Python module to customize a process title
License:        BSD
URL:            http://pypi.python.org/pypi/%{tarname}
Source0:        https://pypi.io/packages/source/s/%{tarname}/%{tarname}-%{version}.tar.gz
%define sha512  setproctitle=9c6d1748685e8b62f9542f73481a587dbe7b6ca157fdcecdd8d2f66bbb71169bf31e47da51867aa0ec9b620c39677ab9a936a7537769714bdc99ef0355c743e0
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Tests
BuildRequires:  python3-pytest
BuildRequires:  procps-ng
%description
Python module allowing a process to change its title as displayed by system tool such as ps and top. It's useful in multiprocess systems, allowing to identify tasks each forked process is busy with. This technique has been used by PostgreSQL and OpenSSH. It's based on PostgreSQL implementation which has proven to be portable.

%package -n python3-%{tarname}
Summary:        Python module to customize a process title
%description -n python3-%{tarname}

%prep
%autosetup -n %{tarname}-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-%{tarname}
%doc README.rst COPYRIGHT
# For arch-specific packages: sitearch
%{python3_sitearch}/%{tarname}*.egg-info

%files
%defattr(-,root,root,-)
%{_lib}/python3.7/site-packages/%{tarname}/*

%changelog
* Tue Jan 17 2023 Anmol Jain <anmolja@gmail.com> 1.3.2-1
- Initial Build
