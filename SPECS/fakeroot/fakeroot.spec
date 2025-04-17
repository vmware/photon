Summary:       Gives a fake root environment
Name:          fakeroot
Version:       1.37.1.1
Release:       1%{?dist}
URL:           https://tracker.debian.org/pkg/fakeroot
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.gz
%define sha512 %{name}=768db08ea9fc6345aeb3604345cb45a6fc588053101fbd5e6f1c43cbf9e5e6fd787f189f0e8b04835ebdcce70935c2b32aa2501ba0079f9cb79c01ad8ad84c97

Source1: license.txt
%include %{SOURCE1}

BuildRequires: libacl-devel
BuildRequires: libcap-devel

%if 0%{?with_check}
# For uudecode
BuildRequires: toybox
%endif

Provides: %{name}-ng = %{version}-%{release}
Obsoletes: %{name}-ng

Requires: %{name}-libs = %{version}-%{release}

%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary: Gives a fake root environment (libraries)

%description libs
This package contains the libraries required by %{name}.

%package docs
Summary: %{name} related man pages

%description docs
%{summary}

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --with-ipc=tcp \
    --libdir=%{_libdir}/lib%{name}

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%make_build check
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/faked

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib%{name}/*.so

%files docs
%defattr(-,root,root,-)
%{_mandir}/*

%changelog
* Fri Apr 11 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.37.1.1-1
- Switch to debian fakeroot
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.18-5
- Release bump for SRP compliance
* Mon Sep 19 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.18-4
- Fix build with latest tool chain
* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.18-3
- Adding BuildArch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.18-2
- GA - Bump release of all rpms
* Fri Jul 10 2015 Luis Zuniga <lzuniga@vmware.com> 0.17-0.1
- Initial build for Photon
