Name:         erlang
Summary:      erlang
Version:      19.3
Release:      1%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com
Source0:      otp_src_%{version}.tar.gz
%define sha1 otp_src=a3be29bff2d258399b1e2fddfc76cf2f6f1efba8
BuildRequires: ncurses-devel

%description
erlang programming language

%prep
%setup -q -n otp_src_%{version}

%build
export ERL_TOP=`pwd`
./otp_build autoconf
./configure --disable-hipe --prefix=%{_prefix}

make

%install

make install DESTDIR=$RPM_BUILD_ROOT

%post

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude /usr/src
%exclude %{_libdir}/debug

%changelog
* Tue Dec 12 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.3-1
- Initial.

