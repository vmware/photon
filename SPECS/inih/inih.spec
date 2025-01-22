Summary:       Simple INI file parser library
Name:          inih
Version:       56
Release:       3%{?dist}
URL:           https://github.com/benhoyt/inih
Group:         System Environment/Development
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:        https://github.com/benhoyt/inih/archive/refs/tags/libinih-%{version}.tar.gz
%define sha512 libinih=ff3e0910990f73e5b21fddc84737ab346279f201c86c7ad864c6cad9de5bde57c3e0a433b9b8f3585b7d86feaae2ea074185f92891dcadc98c274c1c0745d2d2

Source1: license.txt
%include %{SOURCE1}

BuildRequires: meson

%description
The inih package provides simple INI file parser which is only a couple of
pages of code, and it was designed to be small and simple, so it's good for
embedded systems.

%package       devel
Summary:       Header files for libinih
Group:         System Environment/Development
Requires:      %{name} = %{version}-%{release}

%description   devel
This package contains development files for %{name}.

%prep
%autosetup -p1 -n %{name}-r%{version}

%build
%meson
%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
cd tests && bash -x ./unittest.sh
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 56-3
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 56-2
- Release bump for SRP compliance
* Mon Jul 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 56-1
- Initial build. First Version.
- Needed for xfsprogs-5.18.0
