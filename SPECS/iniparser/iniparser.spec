Name:       iniparser
Version:    4.1
Release:    3%{?dist}
Summary:    C library for parsing "INI-style" files
URL:        https://github.com/ndevilla/%{name}
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/ndevilla/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512 %{name}=a8125aaaead1f9dfde380fa1e45bae31ca2312be029f2c53b4072cb3b127d16578a95c7c0aee1e3dda5e7b8db7a865ba6dfe8a1d80eb673061b3babef744e968

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gcc
BuildRequires: make

Patch0: CVE-2025-0633.patch

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%package devel
Summary:    Header files, libraries and development documentation for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1

%build
# remove library rpath from Makefile
sed -i 's|-Wl,-rpath -Wl,/usr/lib||g' Makefile
sed -i 's|-Wl,-rpath,/usr/lib||g' Makefile
# set the CFLAGS to Fedora standard
sed -i 's|^CFLAGS|CFLAGS = %{optflags} -fPIC\nNOCFLAGS|' Makefile

%make_build

%install
install -d %{buildroot}%{_includedir}/%{name} %{buildroot}%{_libdir}
install -m 644 -t %{buildroot}%{_includedir}/%{name} src/dictionary.h src/%{name}.h
ln -s %{name}/dictionary.h %{buildroot}%{_includedir}/dictionary.h
ln -s %{name}/%{name}.h %{buildroot}%{_includedir}/%{name}.h
install -m 755 -t %{buildroot}%{_libdir}/ libiniparser.so.1
ln -s libiniparser.so.1 %{buildroot}%{_libdir}/libiniparser.so

%if 0%{?with_check}
%check
make check %{?_smp_mflags}

cd example && make %{?_smp_mflags}
./iniexample
./parse
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md INSTALL AUTHORS
%license LICENSE
%{_libdir}/libiniparser.so.1

%files devel
%defattr(-,root,root)
%{_libdir}/libiniparser.so
%{_includedir}/%{name}
%{_includedir}/*.h

%changelog
* Fri Feb 21 2025 Mukul Sikka <mukul.sikka@broadcom.com> 4.1-3
- Fix for CVE-2025-0633
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 4.1-2
- Release bump for SRP compliance
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.1-1
- First build. Needed by ndctl v73.
