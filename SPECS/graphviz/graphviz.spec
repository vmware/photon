Name:		graphviz
Summary:	Graph Visualization Tools
Version:	7.0.2
Release:	1%{?dist}
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
License:	EPL-1.0
URL:		http://www.graphviz.org/
Source0:	https://gitlab.com/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 graphviz-7.0.2=04abdd326ce02f45ab0ed0406e91d031b65419c9e11d438ff2e875a2af8ba50efbb4df2067bdd89390c424703ca42e483bd9dd51c6c0cddafa57bfa5e7293170

BuildRequires:  freetype2-devel
BuildRequires:  libgd-devel
BuildRequires:  libpng-devel
BuildRequires:  expat-devel
BuildRequires:  expat-libs
BuildRequires:  fontconfig-devel
BuildRequires:  doxygen
Requires:       doxygen
Requires:       libgd
Requires:       freetype2
Requires:       libpng

%description
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts).

%package devel
Summary:	Development package for graphviz
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes
and edges, not as in barcharts). This package contains development files for
graphviz.

%prep
%autosetup -p1

%build
%configure

%make_build

%install
%make_install docdir=%{_docdir}/%{name}

%check

# upstream test suite
# testsuite seems broken, disabling it for now
# cd rtest
# make rtest

%post
%{?ldconfig}
%{_bindir}/dot -c 2>/dev/null || :

%ldconfig_postun

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gvpr/*
%{_datadir}/%{name}/graphs/*
%exclude %{_docdir}/%{name}/*.html
%exclude %{_docdir}/%{name}/*.pdf

%files devel
%defattr(-,root,root,-)
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/graphviz/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3.*
%{_mandir}/man7/*.7*

%changelog
* Tue Nov 29 2022 Mukul Sikka <msikka@vmware.com> 7.0.2-1
- Initial Build
