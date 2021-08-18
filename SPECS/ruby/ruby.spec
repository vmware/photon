Summary:        Ruby
Name:           ruby
Version:        2.7.3
Release:        2%{?dist}
License:        BSDL
URL:            https://www.ruby-lang.org/en/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://cache.ruby-lang.org/pub/ruby/2.7/%{name}-%{version}.tar.bz2
%define sha1    ruby=4f4a47465b48a91d43fb557b70e47d79f6727a29
Patch0:         CVE-2021-32066.patch
BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
BuildRequires:  tzdata
Requires:       ca-certificates
Requires:       openssl
Requires:       gmp

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%prep
%autosetup -p1

%build
# below loop fixes the files in libexec to point correct ruby
# Only verfied and to be used with ruby version 2.7.1
# Any future versions needs to be verified
for f in `grep -ril "\/usr\/local\/bin\/ruby" ./libexec/`; do
  sed -i "s|/usr/local/bin/ruby|/usr/bin/ruby|g" $f
  head -1 $f
done
%configure \
        --enable-shared \
        --docdir=%{_docdir}/%{name}-%{version} \
	--with-compress-debug-sections=no
make %{?_smp_mflags} COPY="cp -p"

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
%make_install

%check
chmod g+w . -R
useradd test -G root -m
sudo -u test  make check TESTS="-v"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
*   Wed Aug 18 2021 Sujay G <gsujay@vmware.com> 2.7.3-2
-   Fix CVE-2021-32066
*   Wed Apr 07 2021 Sujay G <gsujay@vmware.com> 2.7.3-1
-   Bump version to 2.7.3 to fix CVE-2013-1655
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.7.1-2
-   openssl 1.1.1
*   Tue Sep 01 2020 Sujay G <gsujay@vmware.com> 2.7.1-1
-   Bump version to 2.7.1
*   Fri Jul 17 2020 Ankit Jain <ankitja@vmware.com> 2.5.8-2
-   Added --with-compress-debug-sections=no to fix build issue
*   Wed May 13 2020 Sujay G <gsujay@vmware.com> 2.5.8-1
-   Bump version to 2.5.8
*   Tue Jan 01 2019 Sujay G <gsujay@vmware.com> 2.5.3-1
-   Update to version 2.5.3, to fix CVE-2018-16395 & CVE-2018-16396
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.5.1-1
-   Update to version 2.5.1
*   Fri Jan 12 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-2
-   Fix CVE-2017-17790
*   Wed Jan 03 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-1
-   Update to version 2.4.3, fix CVE-2017-17405
*   Fri Sep 29 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.2-1
-   Update to version 2.4.2
*   Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.1-5
-   [security] CVE-2017-14064
*   Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 2.4.1-4
-   Built with copy preserve mode and fixed %check
*   Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-3
-   [security] CVE-2017-9228
*   Tue Jun 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-2
-   [security] CVE-2017-9224,CVE-2017-9225
-   [security] CVE-2017-9227,CVE-2017-9229
*   Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> 2.4.1-1
-   Update to latest 2.4.1
*   Wed Jan 18 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0-1
-   Update to 2.4.0 - Fixes CVE-2016-2339
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2.3.0-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-3
-   GA - Bump release of all rpms
*   Wed Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> 2.3.0-2
-   Adding readline support
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-1
-   Updated to 2.3.0-1
*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
-   Added SSL support
*   Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
-   Version upgrade to 2.2.1
*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
-   Initial build.  First version
