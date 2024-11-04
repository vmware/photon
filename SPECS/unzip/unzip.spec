Summary:        Unzip-6.0
Name:           unzip
Version:        6.0
Release:        17%{?dist}
URL:            http://www.gnu.org/software/%{name}
Group:          System Environment/Utilities
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/infozip/unzip60.tar.gz
%define sha512 %{name}=0694e403ebc57b37218e00ec1a406cae5cc9c5b52b6798e0d4590840b6cdbf9ddc0d9471f67af783e960f8fa2e620394d51384257dca23d06bcd90224a80ce5d

Source1: license.txt
%include %{SOURCE1}

Patch0:  CVE-2014-9636.patch
Patch1:  CVE-2015-1315.patch
Patch2:  CVE-2015-7696-CVE-2015-7697.patch
Patch3:  CVE-2014-9844.patch
Patch4:  CVE-2014-9913.patch
Patch5:  CVE-2018-18384.patch
Patch6:  CVE-2019-13232-0001-Fix-bug-in-undefer_input-that-misplaced-the-input-st.patch
Patch7:  CVE-2019-13232-0001-Detect-and-reject-a-zip-bomb-using-overlapped-entrie.patch
Patch8:  CVE-2014-8139.patch
Patch9:  CVE-2014-8141.patch
Patch10: CVE-2014-8140.patch
Patch11: CVE-2018-1000035.patch
Patch12: unzip-passwd-as-stdin.patch
Patch13: CVE-2022-0529-2022-0530.patch
Patch14: CVE-2021-4217.patch

%description
The UnZip package contains ZIP extraction utilities. These are useful
for extracting files from ZIP archives. ZIP archives are created
with PKZIP or Info-ZIP utilities, primarily in a DOS environment.

%prep
%autosetup -n unzip60 -p1

%build
sed -i -e 's/CFLAGS="-O -Wall/& -DNO_LCHMOD -DLARGE_FILE_SUPPORT -DZIP64_SUPPORT/' unix/Makefile
sed -i 's/CFLAGS="-O -Wall/CFLAGS="-O -g -Wall/' unix/Makefile
sed -i 's/LF2 = -s/LF2 =/' unix/Makefile
sed -i 's|STRIP = strip|STRIP = /bin/true|' unix/Makefile
%make_build -f unix/Makefile linux_noasm

%install
%make_install -f unix/Makefile prefix="%{buildroot}%{_usr}" %{?_smp_mflags}
ln -sfv unzip %{buildroot}%{_bindir}/zipinfo
rm -rf %{buildroot}%{_usr}/man

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.0-17
- Release bump for SRP compliance
* Mon Jul 24 2023 Nitesh Kumar <kunitesh@vmware.com> 6.0-16
- Patched for CVE-2021-4217
* Fri May 19 2023 Nitesh Kumar <kunitesh@vmware.com> 6.0-15
- Patched for CVE-2022-0529 and CVE-2022-0530
* Tue Apr 21 2020 Sujay G <gsujay@vmware.com> 6.0-14
- Added unzip-passwd-as-stdin.patch
* Tue Apr 21 2020 Sujay G <gsujay@vmware.com> 6.0-13
- Added CVE fixes from patch6 to patch11
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 6.0-12
- Cross compilation support
* Thu Jan 24 2019 Ankit Jain <ankitja@vmware.com> 6.0-11
- Fix for CVE-2018-18384
* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-10
- Fix CVE-2014-9844, CVE-2014-9913
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-9
- Ensure non empty debuginfo
* Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 6.0-8
- Added patch for CVE-2015-7696 and CVE-2015-7697
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 6.0-7
- Modified %check
* Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 6.0-6
- Added patch for CVE-2015-1315
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-5
- GA - Bump release of all rpms
* Tue May 10 2016 Nick Shi <nshi@vmware.com> 6.0-4
- Added unzipsfx, zipgrep and zipinfo to unzip rpm
* Sat Aug 15 2015 Sharath George <sharathg@vmware.com> 6.0-3
- Added patch for CVE-2014-9636
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 6.0-2
- Updated group.
* Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 6.0-1
- Initial build. First version
