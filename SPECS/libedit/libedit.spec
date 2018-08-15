Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.1
Release:	20180525%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	libedit-20180525-3.1.tar.gz
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
%setup -qn libedit-%{release}-%{version}

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
*   Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1-20180525
-   Initial
