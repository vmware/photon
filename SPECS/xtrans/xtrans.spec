Summary:        Abstract network code for X.
Name:           xtrans
Version:        1.4.0
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0:        https://ftp.x.org/pub/individual/lib/xtrans-1.4.0.tar.bz2
%define sha512  xtrans=4fea89a3455c0e13321cbefa43340016dbb59bdd0dbdb5b796c1a6d2a6b1fd63cf1327b769ab426286b9c54b32ec764a50cd2b46228e4e43b841bda6b94de214

BuildRequires:  pkg-config
Provides:       xtrans-devel = %{version}-%{release}

%description
This is a dev package. it contains header and development files

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_datadir}
%{_includedir}

%changelog
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.4.0-1
- Upgrade to 1.4.0
* Wed Feb 12 2020 Alexey Makhalov <amakhalov@vmware.com> 1.3.5-3
- This is purely devel package
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-2
- Updated build requires & requires to build with Photon 2.0
* Mon May 18 2015 Alexey Makhalov <amakhalov@vmware.com> 1.3.5-1
- initial version
