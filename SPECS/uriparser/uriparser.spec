Name:           uriparser
Version:        0.9.7
Release:        2%{?dist}
Summary:        URI parsing library - RFC 3986
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://uriparser.github.io/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha512  uriparser=7f69c9806665745c1bafe11f818434e27c2da03af387f009ef46c1427af8c008faa45e6f49bece66e0b96fd17b3924ba0af25476e796972c5e4b651f35f74c13
Patch0:         remove_dot_dependency.patch
Patch1:         CVE-2024-34402.patch
Patch2:         CVE-2024-34403.patch
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gtest
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  freetype2
BuildRequires:  urw-fonts
Requires:       urw-fonts

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
           -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{_bindir}/uriparse
%{_libdir}/lib%{name}.so.1*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/cmake/%{name}-%{version}/
%{_docdir}/%{name}/html

%changelog
* Mon Jul 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.9.7-2
- Fix CVE-2024-34402, CVE-2024-34403
* Fri Jan 13 2023 Anmol Jain <anmolja@vmware.com> - 0.9.7-1
- Initial Build
