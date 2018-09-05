Summary:     Implementation of a YAML 1.1 parser and emitter
Name:        libyaml
Version:     0.2.1
Release:     1%{?dist}
License:     MIT
Group:       Development/Libraries
URL:         http://pyyaml.org/wiki/LibYAML
Vendor:      VMware, Inc.
Distribution:Photon
Source0:     http://pyyaml.org/download/libyaml/yaml-%{version}.tar.gz
%define      sha1 yaml=125a3113681f06320dcdfde48bab47cba9031263

%description
LibYAML is a C library implementation of a YAML 1.1 parser and emitter.
It includes a Python language binding.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -n yaml-%{version}

%build
%configure --disable-static
%{__make} %{?_smp_mflags} AM_CFLAGS=""

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE README
%{_libdir}/libyaml-0.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/yaml.h
%{_libdir}/libyaml.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.la

%changelog
*       Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.2.1-1
-       Update to version 0.2.1
*       Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.1.7-1
-       Updating version to 0.1.7
*       Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 0.1.6-4
-       Modified check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.6-3
-	GA - Bump release of all rpms
*       Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.6-2
-       Fix cve-2014-9130.
*       Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.6-1
-       Initial package for Photon.
