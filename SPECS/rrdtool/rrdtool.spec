Summary:        Round Robin Database Tool to store and display time-series data
Name:           rrdtool
Version:        1.7.2
Release:        3%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://oss.oetiker.ch/rrdtool/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/oetiker/rrdtool-1.x/releases/download/v1.6.0/%{name}-%{version}.tar.gz
%define sha512 rrdtool=453230efc68aeb4a12842d20a9d246ba478a79c2f6bfd9693a91837c1c1136abe8af177be64fe29aa40bf84ccfce7f2f15296aefe095e89b8b62aef5a7623e29

BuildRequires:  pkg-config
BuildRequires:  libpng-devel
BuildRequires:  pango-devel
BuildRequires:  libxml2-devel
BuildRequires:  pixman-devel
BuildRequires:  freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  cairo-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  systemd

Requires:       systemd

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
        --disable-tcl           \
        --disable-python        \
        --disable-perl          \
        --disable-lua           \
        --disable-examples      \
    --with-systemdsystemunitdir=%{_unitdir} \
    --disable-docs              \
        --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

#%%check
#make %{?_smp_mflags} -k check

%post
/sbin/ldconfig
%systemd_post rrdcached.service

%preun
%systemd_preun rrdcached.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rrdcached.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_unitdir}/rrdcached.service
%{_unitdir}/rrdcached.socket
%exclude %{_datadir}/locale/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.7.2-3
- Bump version as part of glib upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.7.2-2
- Bump version as a part of freetype2 upgrade
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.2-1
- Automatic Version Bump
* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 1.7.0-1
- Updated to version 1.7.0
* Wed Apr 5 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.0-1
- Initial version
