%define majorver 8.6

Summary:         Tool Command Language - the language and library.
Name:            tcl
Version:         8.6.12
Release:         3%{?dist}
URL:             http://tcl.sourceforge.net/
Group:           System Environment/Libraries
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
%define sha512 %{name}=7144a50d19d3855edbda14b538cc94fe26c0dd357b979676c3fe02d599dab61ba777bf14f6aaebb63e238aeff1d0bad25ea7b0ff31b2398468f67fc0a305b9f3

Source1: license.txt
%include %{SOURCE1}

BuildRequires:   cmake

%description
Tcl provides a powerful platform for creating integration applications that
tie together diverse applications, protocols, devices, and frameworks.
When paired with the Tk toolkit, Tcl provides the fastest and most powerful
way to create GUI applications that run on PCs, Unix, and Mac OS X.
Tcl can also be used for a variety of web-related tasks and for creating
powerful command languages for applications.

%package         devel
Summary:         Headers and development libraries for tcl
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}

%description     devel
Headers and development libraries for tcl

%prep
%autosetup -n %{name}%{version}

%build
cd unix
%configure \
       --enable-threads \
       --enable-shared \
       --disable-static \
       --enable-symbols

%make_build

%install
%make_install -C unix %{?_smp_mflags}

ln -sv tclsh%{majorver} %{buildroot}%{_bindir}/tclsh

# for linking with -lib%%{name}
ln -sv lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}%{_libdir}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/%{name}Config.sh %{buildroot}%{_libdir}/%{name}%{majorver}/%{name}Config.sh

mkdir -p %{buildroot}%{_includedir}/%{name}-private/{generic,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}%{_includedir}
  for i in *.h ; do
    [ -f %{buildroot}%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}%{_includedir}/%{name}-private/generic ;
  done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}%{_libdir}/%{name}Config.sh
rm -rf %{buildroot}%{_datadir}/%{name}%{majorver}/ldAix

%if 0%{?with_check}
%check
cd unix && make test %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libtcl%{majorver}.so
%{_libdir}/libtcl.so
%{_libdir}/tcl%{majorver}/*
%{_libdir}/tcl8/*
%{_libdir}/tclConfig.sh
%{_libdir}/tclooConfig.sh
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/tcl.pc
%{_libdir}/libtclstub%{majorver}.a
%{_mandir}/mann/*
%{_mandir}/man3/*
#%%exclude /usr/share/man/man3/Thread.3.gz conflict with package perl-5.28.0-5.ph3.x86_64
%exclude %{_mandir}/man3/Thread.3.gz

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 8.6.12-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 8.6.12-2
- Release bump for SRP compliance
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 8.6.12-1
- Automatic Version Bump
* Thu Jul 15 2021 Nitesh Kumar <kunitesh@vmware.com> 8.6.10-2
- Fix CVE-2021-35331
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 8.6.10-1
- Automatic Version Bump
* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 8.6.8-1
- Update version to 8.6.8.
* Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com>  8.6.6-2
- Package more files (private headers, etc). Took install section from
    Fedora: http://pkgs.fedoraproject.org/cgit/rpms/tcl.git/tree/tcl.spec
- Move init.tcl and other *.tck files to the main package
* Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  8.6.6-1
- Initial build.  First version
