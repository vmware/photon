Name:         erlang
Summary:      erlang
Version:      19.3
Release:      1%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com
BuildArch:    x86_64
Source0:      otp_src_%{version}.tar.gz
%define sha1 otp_src_19.3=6f394857b2910de27b39275cdad9ed05be95bcda

%description
erlang programming language

%prep
%setup -q -n otp_src_%{version}

%build
export ERL_TOP=`pwd`
./otp_build autoconf
./configure --disable-hipe \
    --prefix=%{_prefix}

make

%install

make install DESTDIR=%{buildroot}

%post

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude /usr/src
%exclude %{_libdir}/debug

%changelog
* Fri Mar 31 2017 Chang Lee <changlee@vmware.com> 19.3-1
- Updated Version
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.1-1
- Initial.

