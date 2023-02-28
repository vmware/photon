Summary:        Abstract network code for X.
Name:           xtrans
Version:        1.4.0
Release:        2%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0:        https://ftp.x.org/pub/individual/lib/xtrans-1.4.0.tar.bz2
%define sha512  xtrans=4fea89a3455c0e13321cbefa43340016dbb59bdd0dbdb5b796c1a6d2a6b1fd63cf1327b769ab426286b9c54b32ec764a50cd2b46228e4e43b841bda6b94de214
BuildRequires:  pkg-config

%description
xtrans is a library of code that is shared among various X packages to handle network protocol transport in a modular fashion, allowing a single place to add new transport types. It is used by the X server, libX11, libICE, the X font server, and related components.

%package devel
Summary:        Development package for xtrans
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This is a dev package. it contains header and development files

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%clean
rm -rf %{buildroot}/*

%files
%files devel
%defattr(-,root,root)
%{_datadir}/aclocal
%{_datadir}/pkgconfig
%{_docdir}
%{_includedir}

%changelog
* Wed Mar 01 2023 Harinadh D <hdommaraju@vmware.com> 1.4.0-2
- fix installation error
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 1.4.0-1
- Initial version
