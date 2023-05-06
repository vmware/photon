Summary:    Gperf-3.0.4
Name:       gperf
Version:    3.1
Release:    2%{?dist}
License:    GPLv3+
URL:        https://www.gnu.org/software/gperf
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/gperf/%{name}-%{version}.tar.gz
%define sha512 %{name}=855ebce5ff36753238a44f14c95be7afdc3990b085960345ca2caf1a2db884f7db74d406ce9eec2f4a52abb8a063d4ed000a36b317c9a353ef4e25e2cca9a3f4

%description
Gperf generates a perfect hash function from a key set.

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_docdir}/%{name}-%{version}

%make_build

%install
%make_install %{?_smp_mflags}
install -v -m644 doc/gperf.{dvi,ps,pdf} %{buildroot}/%{_docdir}/%{name}-%{version}
pushd %{buildroot}%{_datadir}/info
for FILENAME in *; do
  install-info $FILENAME %{name}-%{version} 2>/dev/null
done
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
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
- Cross compilation support
* Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 3.1-1
- Updated to version 3.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-2
- GA - Bump release of all rpms
* Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.4-1
- Initial build. First version
