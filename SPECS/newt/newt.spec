Summary:        A library for text mode user interfaces
Name:           newt
Version:        0.52.21
Release:        2%{?dist}
URL:            https://admin.fedoraproject.org/pkgdb/package/newt/
Group:          Development/Languages
Source0:        https://fedorahosted.org/releases/n/e/newt/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       slang
BuildRequires:  slang-devel
BuildRequires:  popt-devel

%description

Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

%package        devel
Summary:        Header and development files for newt
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure \
            --with-gpm-support \
            --without-python \
            --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_libdir}/libnewt.so.0*
%{_bindir}/*
%{_datadir}/*

%files devel
%{_includedir}/*
%{_libdir}/libnewt.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.52.21-2
- Release bump for SRP compliance
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.21-1
- Automatic Version Bump
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.52.20-1
- Update to 0.52.20
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 0.52.18-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.52.18-2
- GA - Bump release of all rpms
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial build. First version
