%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)
# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)

Summary:        Practical Extraction and Report Language
Name:           perl
Version:        5.22.1
Release:        5%{?dist}
License:        GPLv1+
URL:            http://www.perl.org/
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.cpan.org/src/5.0/%{name}-%{version}.tar.bz2
%define sha1    perl=29f9b320b0299577a3e1d02e9e8ef8f26f160332
Patch0:         perl-CVE-2016-1238.patch
Provides:       perl >= 0:5.003000
Provides:       perl(getopts.pl)
Provides:       /bin/perl
BuildRequires:  zlib-devel, bzip2-devel
Requires:       zlib 
Requires:       gdbm
Requires:       glibc
Requires:       libgcc
%description
The Perl package contains the Practical Extraction and
Report Language.
%prep
%setup -q
%patch0 -p1

sed -i 's/-fstack-protector/&-all/' Configure

%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0
CFLAGS="%{_optflags}"

sh Configure -des \
    -Dprefix=%{_prefix} \
    -Dvendorprefix=%{_prefix} \
    -Dman1dir=%{_mandir}/man1 \
    -Dman3dir=%{_mandir}/man3 \
    -Dpager=%{_bindir}"/less -isR" \
    -Duseshrplib \
    -Dusethreads \
        -DPERL_RANDOM_DEVICE="/dev/erandom"

make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
unset BUILD_ZLIB BUILD_BZIP2
%check
make  %{?_smp_mflags} check
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{version}
%{_libdir}/perl5/%{version}/*
%{_mandir}/*/*
%changelog
*   Thu Oct 20 2016 Xiaolin Li <xiaolinl@vmware.com> 5.22.1-5
-   CVE-2016-1238 patch from http://perl5.git.perl.org/perl.git/commit/cee96d52c39b1e7b36e1c62d38bcd8d86e9a41ab.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 5.22.1-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.22.1-3
-   GA - Bump release of all rpms
*   Thu Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-2
-   Enable threads
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-1
-   Update version
*   Thu Jun 4 2015 Touseef Liaqat <tliaqat@vmware.com> 5.18.2-2
-   Provide /bin/perl.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.18.2-1
-   Initial build. First version
