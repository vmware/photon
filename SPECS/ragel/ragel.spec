%define debug_package %{nil}

Name:           ragel
Version:        7.0.4
Release:        2%{?dist}
Summary:        Finite state machine compiler
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/adrian-thurston/ragel

Source0: https://github.com/adrian-thurston/ragel/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=234efc74300877f2bff1e84ffe50bd926c372dee1bab0b734e748e3fc61a6a86d1cfbfb1002e05d4adb70119f9f964ef555fb79f5aab8a12f3e0fc7ae2b23bcc

Source1: license.txt
%include %{SOURCE1}

Patch0: ragel-7.0.4-link-colm-properly.patch

BuildRequires: colm-devel

Requires: gawk
Requires: colm

%description
Ragel compiles finite state machines from regular languages into executable C,
C++, Objective-C, or D code. Ragel state machines can not only recognize byte
sequences as regular expression machines do, but can also execute code at
arbitrary points in the recognition of a regular language. Code embedding is
done using inline operators that do not disrupt the regular language syntax.

%package devel
Summary:    Development libraries header files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure --with-colm=%{_usr} --disable-manual
%make_build

%install
%make_install %{?_smp_mflags}

find %{buildroot}%{_libdir} -type f -name '*.la' -print -delete

mkdir -p %{buildroot}%{_datadir}/vim/vimfiles/syntax/
mv %{buildroot}%{_docdir}/%{name}/%{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/

%if 0%{?with_check}
%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
cd test && ./runtests
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}-*
%{_libdir}/libragel.so.*
%{_datadir}/vim/vimfiles/syntax/%{name}.vim

%files devel
%defattr(-,root,root,-)
%{_mandir}/*/*
%{_libdir}/libragel.a
%{_libdir}/libragel.so
%{_datadir}/*.lm

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.0.4-2
- Release bump for SRP compliance
* Mon Sep 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.0.4-1
- Initial Build
