# Got this spec from http://downloads.sourceforge.net/cracklib/cracklib-2.9.6.tar.gz

Summary:	A password strength-checking library.
Name:		cracklib
Version:	2.9.6
Release:	4%{?dist}
Group:		System Environment/Libraries
Source:		cracklib-%{version}.tar.gz
%define sha1 cracklib-2.9.6=9199e7b8830717565a844430653f5a90a04fcd65
Source1:    cracklib-words-20080507.gz
%define sha1 cracklib-words=e0cea03e505e709b15b8b950d56cb493166607da
URL:		http://sourceforge.net/projects/cracklib/
License:	GPL
Vendor:     VMware, Inc.
Distribution: Photon

BuildRequires: python2 gzip
BuildRequires: python2-libs
BuildRequires: python2-devel

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess. CrackLib
performs certain tests: 

* It tries to generate words from a username and gecos entry and 
  checks those words against the password;
* It checks for simplistic patterns in passwords;
* It checks for the password in a dictionary.

CrackLib is actually a library containing a particular
C function which is used to check the password, as well as
other C functions. CrackLib is not a replacement for a passwd
program; it must be used in conjunction with an existing passwd
program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you
install CrackLib, you'll also want to install the cracklib-dicts
package.

%package	dicts
Summary:	The standard CrackLib dictionaries.
Group:		System Environment/Utilities
Requires:   cracklib

%description	dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%package devel
Summary:	Cracklib link library & header file
Group:		Development/Libraries
Provides:	cracklib-devel
Requires:	cracklib

%description devel
The cracklib devel package include the needed library link and
header files for development.

%package python
Summary:    The cracklib python module
Group:      Development/Languages/Python
Requires:   cracklib
Requires:   python2
Requires:   python2-libs

%description python
The cracklib python module

%package lang
Summary:    The CrackLib language pack.
Group:      System Environment/Libraries

%description lang
The CrackLib language pack.

%prep

%setup -q -n cracklib-%{version}
chmod -R og+rX .
mkdir -p dicts
install %{SOURCE1} dicts/

%build

CFLAGS="$RPM_OPT_FLAGS" ./configure \
  --prefix=%{_prefix} \
  --mandir=%{_mandir} \
  --libdir=%{_libdir} \
  --libexecdir=%{_libdir} \
  --datadir=%{_datadir} \
  --disable-static \
  --with-python

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/
chmod 755 ./util/cracklib-format
chmod 755 ./util/cracklib-packer
util/cracklib-format dicts/cracklib* | util/cracklib-packer $RPM_BUILD_ROOT/%{_datadir}/cracklib/pw_dict
rm -f $RPM_BUILD_ROOT/%{_datadir}/cracklib/cracklib-small
ln -s cracklib-format $RPM_BUILD_ROOT/%{_sbindir}/mkdict
ln -s cracklib-packer $RPM_BUILD_ROOT/%{_sbindir}/packer

%check
mkdir -p /usr/share/cracklib
cp $RPM_BUILD_ROOT%{_datadir}/cracklib/* /usr/share/cracklib/
make %{?_smp_mflags} test

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root)
%{_datadir}/cracklib/cracklib.magic
%{_libdir}/libcrack.so.*

%files devel
%defattr(-,root,root)
%doc README README-DAWG doc
%{_includedir}/*
%{_libdir}/libcrack.so
%{_libdir}/libcrack.la

%files python
%defattr(-,root,root)
%{_libdir}/python*

%files dicts
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/cracklib/pw_dict*

%files lang
%defattr(-,root,root)
%{_datadir}/locale/*

%changelog
*   Sun Nov 20 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-4
-   Revert compressing pw_dict.pwd back. Python code 
    cracklib.VeryFascistCheck does not handle it.
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-3
-   Remove any dicts from cracklib main package
-   Compress pw_dict.pwd file
-   Move doc folder to devel package
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.6-2
-   GA - Bump release of all rpms
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-1
-   Updated to version 2.9.6
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.9.2-2
-   Updated group.

