Summary:        Parallel Implementation of GZip
Name:           pigz
Version:        2.7
Release:        3%{?dist}
Group:          Application/Tools
URL:            https://zlib.net/pigz
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://zlib.net/pigz/pigz-%{version}.tar.gz
%define sha512 %{name}=9f9f61de4a0307fc057dc4e31a98bd8d706d9e709ecde0be02a871534fddf6a1fe1321158aa72708603aaaece43f83d2423b127f7689b6219b23aea4f989e8f5

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  zlib-devel

Requires: zlib

%description
Fully functional replacement for gzip that exploits multiple processors and multiple cores
to the hilt when compressing data.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
mkdir -p \
    %{buildroot}%{_bindir} \
    %{buildroot}%{_mandir} \
    %{buildroot}%{_includedir}
mv %{name} unpigz %{buildroot}%{_bindir}
mv %{name}.1 %{buildroot}%{_mandir}

%check
%if 0%{?with_check}
make test %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/unpigz
%{_mandir}/%{name}.1

%changelog
*   Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.7-3
-   Release bump for SRP compliance
*   Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7-2
-   Bump version as a part of zlib upgrade
*   Wed Apr 27 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.7-1
-   Initial addition to Photon. Modified from provided pigz source version.