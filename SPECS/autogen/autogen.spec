Summary:	The Automated Text and Program Generation Tool
Name:		autogen
Version:	5.18.5
Release:	1%{?dist}
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
Distribution:	Photon
%description
AutoGen is a tool designed to simplify the creation and maintenance of programs that contain large amounts of repetitious text. It is especially valuable in programs that have several blocks of text that must be kept synchronized.

%package devel
Summary:	Development libraries and header files for autogen
Requires:	autogen

%description devel
The package contains libraries and header files for
developing applications that use autogen.

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
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/autogen/*.tlib
%{_datadir}/autogen/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/aclocal/*
%files devel
%defattr(-,root,root)
%{_includedir}/autoopts/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 5.18.5-1
-	Initial build. First version

