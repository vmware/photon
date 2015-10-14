Summary:	The Automated Text and Program Generation Tool
Name:		autogen
Version:	5.18.5
Release:	2%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/autogen/
Source0:        ftp://ftp.gnu.org/gnu/autogen/rel%{version}/%{name}-%{version}.tar.gz
%define sha1 autogen=cd24a7944d646f6aaea5c7ed13018de38c45b3da
Group:		System Environment/Tools
Vendor:		VMware, Inc.
BuildRequires:	guile-devel
BuildRequires:	gc-devel
BuildRequires:	which
#BuildRequires:	libunistring-devel
#BuildRequires:	libltdl-devel
Requires:	guile
Requires:	gc
Requires:	gmp
Requires:   %{name}-libopts
Distribution:	Photon
%description
AutoGen is a tool designed to simplify the creation and maintenance of programs that contain large amounts of repetitious text. It is especially valuable in programs that have several blocks of text that must be kept synchronized.

%package libopts
Summary:	Automated option processing library.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser. 

%package libopts-devel
Summary:	Development files for libopts
License:	LGPLv3+
Group:		Development/Libraries
Requires:	%{name}
Requires:	%{name}-libopts

%description libopts-devel
This package contains development files for libopts.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	libopts -p /sbin/ldconfig
%postun	libopts -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/autoopts-config
%{_libdir}/autogen/*.tlib
%{_datadir}/autogen/*
%{_mandir}/man1/*
%exclude %{_mandir}/man1/autoopts-config.1.gz


%files libopts
%{_libdir}/*.so.*

%files libopts-devel
%defattr(-,root,root)
%{_includedir}/autoopts/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_bindir}/autoopts-config
%{_datadir}/aclocal/*
%{_mandir}/man1/autoopts-config.1.gz
%{_mandir}/man3/*
%{_libdir}/*.a
%{_libdir}/*.la

%changelog
*   Tue Sep 29 2015 Xiaolin Li <xiaolinl@vmware.com> 5.18.5-2
-   Create a seperate libopts package.
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 5.18.5-1
-	Initial build. First version

