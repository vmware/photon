Summary:        C++ interface to the glib
Name:           glibmm
Version:        2.74.0
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://ftp.gnome.org/pub/GNOME/sources/glibmm
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.74/%{name}-%{version}.tar.xz
%define sha512 %{name}=29c16a6c921fb135721c39b5328e0b45e09c500c65175199c1ec5ee75bdd5fb907072389c6980da3bf8fac0846235af5580f692706eb00d26947804daa1c99c9

BuildRequires:  python3-devel
BuildRequires:  libsigc++-devel >= 3.2.0
BuildRequires:  glib-devel >= 2.74.1
BuildRequires:  glib-schemas >= 2.74.1
BuildRequires:  meson

%if 0%{?with_check}
BuildRequires:  glib-networking
%endif

Requires:       libsigc++ >= 3.2.0
Requires:       glib >= 2.74.1
Requires:       gobject-introspection >= 1.74.0
Requires:       XML-Parser
Requires:       perl

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.

%package        devel
Summary:        Header files for glibmm
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.74.1
Requires:       libsigc++ >= 3.2.0

%description    devel
These are the header files of glibmm.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/glibmm-2.68/proc/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/glibmm-2.68/include/*
%{_libdir}/giomm-2.68/include/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.74.0-1
- Upgrade to v2.74.0
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.65.3-2
- Remove .la files
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.65.3-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 2.56.0-2
- Build with python3
- Mass removal python2
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.56.0-1
- Update to version 2.56.0
* Thu Aug 24 2017 Rongrong Qiu <rqiu@vmware.com> 2.50.1-2
- add buildrequires for make check for bug 1900286
* Fri May 26 2017 Harish Udaiya Kumar <hudaiykumar@vmware.com> 2.50.1-1
- Downgrade to stable version 2.50.1
* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.53.1-1
- Update to version 2.53.1
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.1-2
- Modified %check
* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.1-1
- Updated to version 2.48.1-1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.3.1-2
- GA - Bump release of all rpms
* Thu Apr 14 2016 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.3.1-1
- Updated to version 2.47.3.1
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.46.3-1
- Updated to version 2.46.3
* Tue Jul 7 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
- Created devel subpackage. Added Summary.
* Tue Jun 23 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
- Added glib-schemas to build requirements.
* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
- Initial version
