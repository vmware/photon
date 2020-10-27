Summary:       jq is a lightweight and flexible command-line JSON processor.
Name:          jq
Version:       1.6
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/stedolan/jq
Source0:       https://github.com/stedolan/jq/releases/download/jq-%{version}/jq-%{version}.tar.gz
%define sha1 jq=73bcbdc45be4db907a864e829b06cd869f77f4f7
Distribution:  Photon
%if %{with_check}
BuildRequires: which

%endif

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary:    Development files for jq
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jq

%prep
%setup -n %{name}-%{version}

%build
autoreconf -fi
%configure --with-oniguruma=no --disable-static
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
*  Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 1.6-2
-  Removed bundled oniguruma library
*  Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6-1
-  Automatic Version Bump
*  Mon Nov 19 2018 Ashwin H<ashwinh@vmware.com> 1.5-4
-  Add which for %check
*  Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 1.5-3
-  Add oniguruma for %check
*  Wed Jun 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5-2
-  Fix for CVE-2015-8863 and CVE-2016-4074
*  Mon May 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5-1
-  Initial version
