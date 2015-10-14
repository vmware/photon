Summary:	Contains a utility for determining file types
Name:		file
Version:	5.22
Release:	2%{?dist}
License:	BSD
URL:		http://www.darwinsys.com/file
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1 file=20fa06592291555f2b478ea2fb70b53e9e8d1f7c
%description
The package contains a utility for determining the type of a
given file or files

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files and documentation for developing applications that use %{name}.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/*/*
%{_datarootdir}/misc/magic.mgc

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 5.22-2
-   Move development libraries and header files to devel package.
*	Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-	Initial build. First version
