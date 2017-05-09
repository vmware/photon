Name:          c-rest-engine
Summary:       minimal http(s) server library
Version:       1.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           http://www.github.com/vmware/c-rest-engine
BuildArch:     x86_64
Requires:      coreutils >= 8.22
Requires:      openssl >= 1.0.1
BuildRequires: coreutils >= 8.22
BuildRequires: openssl-devel >= 1.0.1
Source0:       %{name}-%{version}.tar.gz
%define sha1   c-rest-engine=8187a0dd164bc97e97d284d23d849d6615204227

%description
c-rest-engine is a minimal embedded http(s) server written in C.
Its primary intent is to enable REST(Representational State Transfer)
API support for C daemons.

%package devel
Summary: c-rest-engine dev files
Requires:  coreutils >= 8.22
Requires:  openssl-devel >= 1.0.1
Requires:  %{name} = %{version}-%{release}

%description devel
development libs and header files for c-rest-engine

%prep
%setup -q

%build
cd build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix} \
    --with-ssl=/usr \
    --enable-debug=%{_enable_debug} \
    --disable-static

make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build && make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_includedir}/%{name}
find %{buildroot} -name '*.la' -delete
mv $RPM_BUILD_ROOT/%{_includedir}/vmrest.h $RPM_BUILD_ROOT/%{_includedir}/%{name}


%post -p  /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%exclude %{_sbindir}/vmrestd

%files devel
%{_includedir}/%{name}/vmrest.h
%{_libdir}/*.so

# %doc ChangeLog README COPYING

%changelog
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-1
-  Initial build.  First version
