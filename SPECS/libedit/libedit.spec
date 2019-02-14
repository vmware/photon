
%define libedit_version 3.1
%define libedit_release 20180525

Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.1.20180525
Release:	1%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	libedit-%{libedit_release}-%{libedit_version}.tar.gz
%define sha1    libedit=cf6eb4f32c0336f0f3de68afbcdbeaa4d70b42b6
License:	BSD
Url:		http://www.thrysoee.dk/editline/
Group:		Applications/Libraries
Requires:       ncurses
BuildRequires:  ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD
Editline library. It provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

%package        devel
Summary:        The NetBSD Editline library
Group:          Development/Libraries
Requires:       libedit = %{version}-%{release}

%description devel
Development files for libedit

%prep
%setup -qn libedit-%{libedit_release}-%{libedit_version}

%build
./configure \
--prefix=%{_prefix} \
--disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    %{_libdir}/*.so.*
    %{_mandir}/*

%files devel
    %defattr(-,root,root,0755)
    %{_libdir}/*.so
    %{_libdir}/pkgconfig
    %{_includedir}/*

%changelog
*   Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.20180525-1
-   Initial
