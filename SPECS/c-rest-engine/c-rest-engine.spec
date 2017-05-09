Name:          c-rest-engine
Summary:       VMware REST Library
Version:       0.0.1
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           http://www.github.com/vmware/c-rest-engine
BuildArch:     x86_64
Requires:      coreutils >= 8.22, openssl >= 1.0.1
BuildRequires: coreutils >= 8.22, openssl-devel >= 1.0.1
Source0:       %{name}-%{version}.tar.gz
%define sha1   c-rest-engine=2b6852332400b35962630a2524063f943b6ff69e

%description
VMware REST Library

%package devel
Summary: VMware REST Library
Requires:  coreutils >= 8.22, openssl >= 1.0.1, %{name} = %{version}-%{release}
BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1

%description devel
VMware REST library devel

%prep
%setup -q

%build
cd build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_lib64dir} \
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
%exclude %{_sbindir}/vmrestd
%{_lib64dir}/*.so.*
%exclude  /usr/sbin/vmresttest

%files devel
%{_includedir}/%{name}/vmrest.h
%{_lib64dir}/*.so

# %doc ChangeLog README COPYING

%changelog
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-1
-  Initial build.  First version
