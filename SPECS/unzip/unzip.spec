Summary:        Unzip-6.0
Name:           unzip
Version:        6.0
Release:        11%{?dist}
License:        BSD
URL:            http://www.gnu.org/software/%{name}
Source0:        http://downloads.sourceforge.net/infozip/unzip60.tar.gz
%define sha1    unzip=abf7de8a4018a983590ed6f5cbd990d4740f8a22
Group:          System Environment/Utilities
Vendor:         VMware, Inc.
Distribution:   Photon

Patch0:         cve-2014-9636.patch
Patch1:         cve-2015-1315.patch
Patch2:         CVE-2015-7696-CVE-2015-7697.patch
Patch3:         unzip-CVE-2014-9844.patch
Patch4:         unzip-CVE-2014-9913.patch
Patch5:         unzip_cfactor_overflow.patch

%description
The UnZip package contains ZIP extraction utilities. These are useful
for extracting files from ZIP archives. ZIP archives are created
with PKZIP or Info-ZIP utilities, primarily in a DOS environment.

%prep
%setup -qn unzip60
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
case `uname -m` in
  i?86)
    sed -i -e 's/DASM_CRC"/DASM_CRC -DNO_LCHMOD"/' unix/Makefile
    make -f unix/Makefile linux %{?_smp_mflags}
    ;;
  *)
    sed -i -e 's/CFLAGS="-O -Wall/& -DNO_LCHMOD/' unix/Makefile
    sed -i 's/CFLAGS="-O -Wall/CFLAGS="-O -g -Wall/' unix/Makefile
    sed -i 's/LF2 = -s/LF2 =/' unix/Makefile
    sed -i 's|STRIP = strip|STRIP = /bin/true|' unix/Makefile
    make -f unix/Makefile linux_noasm %{?_smp_mflags}
    ;;
esac

%install
install -v -m755 -d %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} prefix=%{_prefix} install
cp %{_builddir}/unzip60/funzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzipsfx %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unix/zipgrep %{buildroot}%{_bindir}
ln -sf unzip %{buildroot}%{_bindir}/zipinfo

%check
make %{?_smp_mflags}  check

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
*   Thu Jan 24 2019 Ankit Jain <ankitja@vmware.com> 6.0-11
-   Fix for CVE-2018-18384
*   Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-10
-   Fix CVE-2014-9844, CVE-2014-9913
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-9
-   Ensure non empty debuginfo
*   Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 6.0-8
-   Added patch for CVE-2015-7696 and CVE-2015-7697
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 6.0-7
-   Modified %check
*   Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 6.0-6
-   Added patch for CVE-2015-1315
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-5
-   GA - Bump release of all rpms
*   Tue May 10 2016 Nick Shi <nshi@vmware.com> 6.0-4
-   Added unzipsfx, zipgrep and zipinfo to unzip rpm
*   Sat Aug 15 2015 Sharath George <sharathg@vmware.com> 6.0-3
-   Added patch for CVE-2014-9636
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 6.0-2
-   Updated group.
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 6.0-1
-   Initial build. First version
