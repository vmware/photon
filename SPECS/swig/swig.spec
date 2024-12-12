Summary:        Connects C/C++/Objective C to some high-level programming languages
Name:           swig
Version:        4.1.1
Release:        3%{?dist}
URL:            http://swig.sourceforge.net/
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages

Source0: http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz
%define sha512 %{name}=1cea1918455a75ebc9b2653dd1715bd5dcd974554955f324295c6a6f14c0a715651b221b85fad4a8af5197e0c75bfe7b590bc6ba7178c26245fbbd9a7e110100

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  pcre2-devel
Requires:       pcre2

%description
Simplified Wrapper and Interface Generator (SWIG) is a software
development tool for connecting C, C++ and Objective C programs with a
variety of high-level programming languages.  SWIG is primarily used
with Perl, Python and Tcl/TK, but it has also been extended to Java,
Eiffel and Guile. SWIG is normally used to create high-level
interpreted programming environments, systems integration, and as a
tool for building user interfaces

%prep
%autosetup -n %{name}-%{version}

%build
./autogen.sh
%configure \
    --without-ocaml \
    --without-java \
    --without-r \
    --without-go
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

# Enable ccache-swig by default, if ccache is installed.
mkdir -p %{buildroot}%{_libdir}/ccache
ln -fs ../../bin/ccache-swig %{buildroot}%{_libdir}/ccache/swig

%check
make %{?_smp_mflags} check

%files
%{_bindir}/*
%{_datadir}/swig
%{_libdir}/ccache

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 4.1.1-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.1.1-2
- Release bump for SRP compliance
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 4.1.1-1
- Automatic Version Bump
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.2-1
- Automatic Version Bump
* Tue May 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.12-2
- Correct the license.
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.12-1
- Update to version 3.0.12
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.0.8-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.8-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  3.0.8-1
- Upgrade to 3.0.8
* Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 3.0.5-1
- Initial version
