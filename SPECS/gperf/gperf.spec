Summary:    Gperf-3.0.4
Name:       gperf
Version:    3.1
Release:    4%{?dist}
URL:        https://www.gnu.org/software/gperf
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://ftp.gnu.org/gnu/gperf/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
Gperf generates a perfect hash function from a key set.

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -v -m644 doc/gperf.{dvi,ps,pdf} %{buildroot}/%{_docdir}/%{name}-%{version}
pushd  %{buildroot}/usr/share/info &&
  for FILENAME in *; do
    install-info $FILENAME %{name}-%{version} 2>/dev/null
  done &&
popd

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*
%{_datadir}/info/*
%{_bindir}/*

%changelog
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.1-4
-   Release bump for SRP compliance
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1-3
-   Release bump for SRP compliance
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
-   Cross compilation support
*   Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 3.1-1
-   Updated to version 3.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-2
-   GA - Bump release of all rpms
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.4-1
-   Initial build. First version
