Summary:	An interpreted language that may be embedded into an application to make the application extensible.
Name:		slang
Version:	2.2.4
Release:	1%{?dist}
License:	GNU General Public License
URL:		http://www.jedsoft.org/slang/index.html
Group:		Development/Languages
Source0:	http://www.jedsoft.org/releases/slang/old/%{name}-%{version}.tar.bz2
%define sha1 slang=34e68a993888d0ae2ebc7bc31b40bc894813a7e2
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: readline-devel

%description
S-Lang is a multi-platform programmer's library designed to allow a developer to create robust multi-platform software. It provides facilities required by interactive applications such as display/screen management, keyboard input, keymaps, and so on. The most exciting feature of the library is the slang interpreter that may be easily embedded into a program to make it extensible. While the emphasis has always been on the embedded nature of the interpreter, it may also be used in a stand-alone fashion through the use of slsh, which is part of the S-Lang distribution.

Unlike many interpreters, the S-Lang interpreter supports all of the native C integer types (signed and unsigned versions of char, short, int, long, and long long), and both single and double precision types, as well as a double precision complex type. Other data types supported by the interpreter include strings, lists, associative arrays (hashes), user-defined structures, and multi-dimensional arrays of any data-type.

The S-Lang interpreter has very strong support for array-based operations making it ideal for numerical applications.

%package	devel
Summary:	Header and development files for ncurses
Requires:	%{name} = %{version}

%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --with-readline=gnu
make -j1

%install
make DESTDIR=%{buildroot} install_doc_dir=%{_docdir}/slang-2.2.4   \
     SLSH_DOC_DIR=%{_docdir}/slang-2.2.4/slsh \
     install-all

chmod -v 755 %{buildroot}%{_libdir}/libslang.so.2.2.4 \
             %{buildroot}%{_libdir}/slang/v2/modules/*.so

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_libdir}/slang/*
%{_libdir}/libslang.so.2*
%{_bindir}/*
%{_datadir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/libslang.so
%{_libdir}/pkgconfig/*.pc


%changelog
*	Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-	Initial build.	First version
