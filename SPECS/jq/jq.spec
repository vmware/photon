Summary:       jq is a lightweight and flexible command-line JSON processor.
Name:          jq
Version:       1.5
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/stedolan/jq
Source0:       https://github.com/stedolan/jq/releases/download/jq-1.5/jq-1.5.tar.gz
%define sha1 jq=6eef3705ac0a322e8aa0521c57ce339671838277
Distribution:  Photon

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary:    Development files for jq
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jq

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/*
%{_datadir}/*
%{_libdir}/libjq.so.*

%files devel
%{_libdir}/libjq.so
%{_includedir}/*

%changelog
*  Mon May 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5-1
-  Initial version
