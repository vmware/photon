Summary:	Connects C/C++/Objective C to some high-level programming languages
Name:		swig
Version:	3.0.5
Release:	1%{?dist}
License:	GPLv3+ and BSD
URL:		http://swig.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
%define sha1 swig=271813b317e4836853d2249fc8ce2df34c2a062a
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	pcre-devel
Requires:	pcre

%description
Simplified Wrapper and Interface Generator (SWIG) is a software
development tool for connecting C, C++ and Objective C programs with a
variety of high-level programming languages.  SWIG is primarily used
with Perl, Python and Tcl/TK, but it has also been extended to Java,
Eiffel and Guile. SWIG is normally used to create high-level
interpreted programming environments, systems integration, and as a
tool for building user interfaces

%prep
%setup -q -n swig-%{version}

%build
./autogen.sh

%configure \
	--without-ocaml \
 	--without-java \
 	--without-r \
 	--without-go

make %{?_smp_mflags}

%install

make DESTDIR=%{buildroot} install

# Enable ccache-swig by default, if ccache is installed.
mkdir -p %{buildroot}%{_libdir}/ccache
ln -fs ../../bin/ccache-swig %{buildroot}%{_libdir}/ccache/swig

%files
%{_bindir}/*
%{_datadir}/swig
%{_libdir}/ccache
%{_mandir}/man1/*

%changelog
* Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 3.05-1
- Initial version


