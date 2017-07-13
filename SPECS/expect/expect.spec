Summary:        Expect is a tool for automating interactive applications
Name:           expect
Version:        5.45
Release:        1%{?dist}
License:        GPLv2+
URL:            https://sourceforge.net/projects/expect
Source0:        http://prdownloads.sourceforge.net/expect/expect5.45.tar.gz
%define sha1    expect=e634992cab35b7c6931e1f21fbb8f74d464bd496
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       tcl
BuildRequires:  tcl-devel
%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. Expect is also useful
for testing these same applications.

%package devel
Summary: Headers and development libraries for expect
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel

%description devel
Headers and development libraries for expect

%prep
%setup -q -n %{name}%{version} 

%build
./configure \
    --prefix=%{_prefix} \
    --mandir=/usr/share/man

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*


%changelog
*   Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-1
-   Initial build. First version
