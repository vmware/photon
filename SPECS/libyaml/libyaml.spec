Summary:     Implementation of a YAML 1.1 parser and emitter
Name:        libyaml
Version:     0.2.5
Release:     1%{?dist}
License:     MIT
Group:       Development/Libraries
URL:         http://pyyaml.org/wiki/LibYAML
Vendor:      VMware, Inc.
Distribution:   Photon

Source0: http://pyyaml.org/download/libyaml/yaml-%{version}.tar.gz
%define sha512 yaml=dadd7d8e0d88b5ebab005e5d521d56d541580198aa497370966b98c904586e642a1cd4f3881094eb57624f218d50db77417bbfd0ffdce50340f011e35e8c4c02

%description
LibYAML is a C library implementation of a YAML 1.1 parser and emitter.
It includes a Python language binding.

%package devel
Summary:    Header files, libraries and development documentation for %{name}.
Group:      Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1 -n yaml-%{version}

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_libdir}/libyaml-0.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/yaml.h
%{_libdir}/libyaml.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.5-1
- Automatic Version Bump
* Thu Aug 22 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.2.1-2
- Fix PyYAML make check
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.2.1-1
- Update to version 0.2.1
* Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 0.1.7-1
- Updating version to 0.1.7
* Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 0.1.6-4
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.6-3
- GA - Bump release of all rpms
* Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.6-2
- Fix cve-2014-9130.
* Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.6-1
- Initial package for Photon.
