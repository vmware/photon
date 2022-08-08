Name:           colm
Version:        0.14.7
Release:        1%{?dist}
Summary:        Programming language designed for the analysis of computer languages
# aapl/ and some headers from src/ are the LGPLv2+
License:        MIT and LGPLv2+
URL:            https://github.com/adrian-thurston/colm
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/adrian-thurston/colm/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=9328689be147ec5310a45e5a1adf8e420c01cc5c1a10def22229721698fabb320d99f4ecd3a599b1d92abc75e579d46a73a6a1fc16f9c6c46f1f5da9c39cbdf4

Patch0: colm-0.14.7-disable-static-lib.patch

BuildRequires:  build-essential
BuildRequires:  asciidoc3

%description
Colm is a programming language designed for the analysis and transformation
of computer languages. Colm is influenced primarily by TXL. It is
in the family of program transformation languages.

%package devel
Summary:    Development libraries and header files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure --disable-manual --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

find %{buildroot} -type f -name '*.la' -print -delete

mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_datadir}/*.lm %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_datadir}/runtests %{buildroot}%{_datadir}/%{name}

ln -sfv %{buildroot}%{_libdir}/lib%{name}-%{version}.so %{_libdir}/lib%{name}.so

mkdir -p %{buildroot}%{_datadir}/vim/vimfiles/syntax/
mv %{buildroot}%{_docdir}/%{name}/%{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/

%ldconfig_scriptlets

%if 0%{?with_check}
%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
cd test && ./runtests
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}-wrap
%{_libdir}/libcolm-%{version}.so
%{_libdir}/libfsm-%{version}.so
%{_datadir}/vim/vimfiles/syntax/%{name}.vim

%files devel
%defattr(-,root,root,-)
%{_libdir}/libfsm.so
%{_libdir}/libcolm.so
%{_datadir}/%{name}/*.lm
%{_datadir}/%{name}/runtests
%{_includedir}/%{name}/
%{_includedir}/aapl/*.h
%{_includedir}/libfsm/*.h

%changelog
* Mon Sep 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.14.7-1
- Initial build, needed for ragel.
