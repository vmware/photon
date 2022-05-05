%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        rt-tests tests various real-time features of linux
Name:           rt-tests
Version:        2.3
Release:        1%{?dist}
License:        GPL-3.0
Group:          Development/Tools
URL:            https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/
Source0:        %{name}-%{version}.tar.gz
%define sha512  rt-tests=920e04c716a104b08c49ab5886723d68064c7a28a65078201198c3edb695d07e491ed05f62615400efa13b0ece3a74b82037aa23fec9e3b3e9577cc9686e0ed4
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  build-essential
BuildRequires:  libnuma-devel
BuildRequires:  python3
Requires:       python3
Requires:       libnuma
Requires:       glibc

%description
rt-tests includes various programs that test different real-time
features of the linux kernel. Refer to documentation on each test
for detailed descriptions.

%prep
%autosetup -n %{name}-%{version}

%build
make %{?_smp_mflags} prefix=%{_prefix}

%install
make %{?_smp_mflags} install prefix=%{_prefix} DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{python3_sitelib}/hwlatdetect.py
%{python3_sitelib}/get_cyclictest_snapshot.py
%{_mandir}/man8/*

%changelog
* Thu May 05 2022 Sharan Turlapati <sturlapati@vmware.com> 2.3-1
- Initial version of rt-tests for Photon
