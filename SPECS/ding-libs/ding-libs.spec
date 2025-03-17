Name:           ding-libs
Version:        0.6.2
Release:        2%{?dist}
Summary:        "Ding is not GLib" assorted utility libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Libraries
URL:            https://github.com/SSSD/ding-libs

Source0: https://github.com/SSSD/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# ding-libs is a meta-package that will pull in all of its own
# sub-packages

# Cannot set different version numbers for subpackages, otherwise build process fails
Requires: libpath-utils = %{version}-%{release}
Requires: libdhash = %{version}-%{release}
Requires: libcollection = %{version}-%{release}
Requires: libref-array = %{version}-%{release}
Requires: libini-config = %{version}-%{release}

BuildRequires: build-essential
BuildRequires: m4
BuildRequires: pkg-config
BuildRequires: check
BuildRequires: gettext
BuildRequires: readline-devel

%description
A meta-package that pulls in libcollection, libdhash, libini-config,
librefarray and libpath-utils.

%package devel
Summary: Development packages for ding-libs
Group: Development/Libraries

Requires: %{name} = %{version}-%{release}
Requires: libpath-utils-devel = %{version}-%{release}
Requires: libdhash-devel = %{version}-%{release}
Requires: libcollection-devel = %{version}-%{release}
Requires: libref-array-devel = %{version}-%{release}
Requires: libbasicobjects-devel = %{version}-%{release}
Requires: libini-config-devel = %{version}-%{release}

%description devel
Header files for ding-libs.

%package -n libpath-utils
Summary: Filesystem Path Utilities
Group: Development/Libraries

%description -n libpath-utils
Utility functions to manipulate filesystem pathnames

%package -n libpath-utils-devel
Summary: Development files for libpath-utils
Group: Development/Libraries
Requires: libpath-utils = %{version}-%{release}

%description -n libpath-utils-devel
Utility functions to manipulate filesystem pathnames

%package -n libdhash
Group: Development/Libraries
Summary: Dynamic hash table

%description -n libdhash
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%package -n libdhash-devel
Summary: Development files for libdhash
Group: Development/Libraries
Requires: libdhash = %{version}-%{release}

%description -n libdhash-devel
A hash table which will dynamically resize to achieve optimal storage & access
time properties

%package -n libcollection
Summary: Collection data-type for C
Group: Development/Libraries

%description -n libcollection
A data-type to collect data in a hierarchical structure for easy iteration
and serialization

%package -n libcollection-devel
Summary: Development files for libcollection
Group: Development/Libraries
Requires: libcollection = %{version}-%{release}

%description -n libcollection-devel
Header/development files for libcollection.

%package -n libref-array
Summary: A refcounted array for C
Group: Development/Libraries

%description -n libref-array
A dynamically-growing, reference-counted array

%package -n libref-array-devel
Summary: Development files for libref-array
Group: Development/Libraries
Requires: libref-array = %{version}-%{release}

%description -n libref-array-devel
Header/development files for libref-array

%package -n libbasicobjects
Summary: Basic object types for C
Group: Development/Libraries

%description -n libbasicobjects
Basic object types

%package -n libbasicobjects-devel
Summary: Development files for libbasicobjects
Group: Development/Libraries
Requires: libbasicobjects = %{version}-%{release}

%description -n libbasicobjects-devel
Headers/development files for libbasicobjects

%package -n libini-config
Summary: INI file parser for C
Group: Development/Libraries
Requires: libcollection = %{version}-%{release}
Requires: libref-array = %{version}-%{release}
Requires: libbasicobjects = %{version}-%{release}
Requires: libpath-utils = %{version}-%{release}

%description -n libini-config
Library to process config files in INI format into a libcollection data
structure

%package -n libini-config-devel
Summary: Development files for libini-config
Group: Development/Libraries
Requires: libini-config = %{version}-%{release}
Requires: libcollection-devel = %{version}-%{release}
Requires: libref-array-devel = %{version}-%{release}
Requires: libbasicobjects-devel = %{version}-%{release}

%description -n libini-config-devel
Header/development files for libini-config.

%prep
%autosetup

%build
autoreconf -ivf
%configure --disable-static

%make_build all docs

%install
%make_install %{?_smp_mflags}

# Remove document install script. RPM is handling this
rm -f */doc/html/installdox

# Remove docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}/*

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

%files devel
%defattr(-,root,root,-)

%files -n libpath-utils
%defattr(-,root,root,-)
%{_libdir}/libpath_utils.so.1
%{_libdir}/libpath_utils.so.1.0.1

%files -n libpath-utils-devel
%defattr(-,root,root,-)
%{_includedir}/path_utils.h
%{_libdir}/libpath_utils.so
%{_libdir}/pkgconfig/path_utils.pc
%doc path_utils/README.path_utils

%files -n libdhash
%defattr(-,root,root,-)
%{_libdir}/libdhash.so.1
%{_libdir}/libdhash.so.1.1.0

%files -n libdhash-devel
%defattr(-,root,root,-)
%{_includedir}/dhash.h
%{_libdir}/libdhash.so
%{_libdir}/pkgconfig/dhash.pc
%doc dhash/README.dhash
%doc dhash/examples/*.c

%files -n libcollection
%defattr(-,root,root,-)
%{_libdir}/libcollection.so.4
%{_libdir}/libcollection.so.4.1.1

%files -n libcollection-devel
%defattr(-,root,root,-)
%{_includedir}/collection.h
%{_includedir}/collection_tools.h
%{_includedir}/collection_queue.h
%{_includedir}/collection_stack.h
%{_libdir}/libcollection.so
%{_libdir}/pkgconfig/collection.pc

%files -n libref-array
%defattr(-,root,root,-)
%{_libdir}/libref_array.so.1
%{_libdir}/libref_array.so.1.2.1

%files -n libref-array-devel
%defattr(-,root,root,-)
%{_includedir}/ref_array.h
%{_libdir}/libref_array.so
%{_libdir}/pkgconfig/ref_array.pc
%doc refarray/README.ref_array

%files -n libbasicobjects
%defattr(-,root,root,-)
%{_libdir}/libbasicobjects.so.0
%{_libdir}/libbasicobjects.so.0.1.0

%files -n libbasicobjects-devel
%defattr(-,root,root,-)
%{_includedir}/simplebuffer.h
%{_libdir}/libbasicobjects.so
%{_libdir}/pkgconfig/basicobjects.pc

%files -n libini-config
%defattr(-,root,root,-)
%{_libdir}/libini_config.so.5
%{_libdir}/libini_config.so.5.2.1

%files -n libini-config-devel
%defattr(-,root,root,-)
%{_includedir}/ini_config.h
%{_includedir}/ini_configobj.h
%{_includedir}/ini_valueobj.h
%{_includedir}/ini_comment.h
%{_includedir}/ini_configmod.h
%{_libdir}/libini_config.so
%{_libdir}/pkgconfig/ini_config.pc

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.6.2-2
- Release bump for SRP compliance
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.6.2-1
- Initial addition to Photon. Needed for addition of SSSD.
- Modified from provided spec file in GitHub repository.
