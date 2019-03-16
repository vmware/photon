%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: 	Creates a common metadata repository
Name: 		createrepo
Version: 	0.10.4
Release: 	3%{?dist}
License:	GPLv2+
Group: 		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0: 	%{name}-%{version}.tar.gz
%define sha1 createrepo=b4e88b3a8cb4b4ef7154991d33948e3d05bd9663
URL: 		http://createrepo.baseurl.org/download/
BuildArch: noarch
Requires: python2 >= 2.1, rpm-devel, rpm >= 0:4.1.1, libxml2
Requires: yum-metadata-parser, yum >= 3.2.7
Requires: bash
Requires: deltarpm
BuildRequires: bash
BuildRequires: deltarpm
BuildRequires: yum-metadata-parser, yum, rpm-devel, rpm, libxml2, python2, python2-libs
%description
This utility will generate a common metadata repository from a directory of
rpm packages

%prep
%setup -q

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%dir %{_datadir}/%{name}
%doc ChangeLog README COPYING COPYING.lib
%{_datadir}/%{name}/*
%{_datadir}/man/*
%{_bindir}/%{name}
%{_bindir}/mergerepo
%{_bindir}/modifyrepo
%{_mandir}/man8/createrepo.8*
%{_mandir}/man1/modifyrepo.1*
/etc/bash_completion.d/*
%{python_sitelib}/createrepo

%changelog
* Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 0.10.4-3
- Replaced BuildArchitecture to BuildArch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.10.4-2
-	GA - Bump release of all rpms
* Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.10.4
- Updating to new version.
* Thu Dec 20 2007 Seth Vidal <skvidal at fedoraproject.org>
- beginning of the new version

* Mon Dec  3 2007 Luke Macken <lmacken@redhat.com>
- Add man page for modifyrepo

* Thu Jun 07 2007 Paul Nasrat <pnasrat at redhat.com>
- 0.4.10

* Wed May 16 2007 Paul Nasrat <pnasrat at redhat.com>
- 0.4.9

* Mon Feb 12 2007 Seth Vidal <skvidal at linux.duke.edu>
- 0.4.8

* Tue Feb  6 2007 Seth Vidal <skvidal at linux.duke.edu>
- 0.4.7 and yum-metadata-parser dependency

* Sat Oct 14 2006 Luke Macken <lmacken@redhat.com>
- Add modifyrepo

* Fri Aug 11 2006 Paul Nasrat <pnasrat@redhat.com>
- 0.4.6

* Wed Jul 19 2006 Luke Macken <lmacken@redhat.com>
- Remove python-urlgrabber dependency

* Fri Jun  9 2006 Seth Vidal <skvidal at linux.duke.edu>
- 0.4.5

* Sat Mar 04 2006 Paul Nasrat <pnasrat@redhat.com>
- 0.4.4

* Thu Jul 14 2005 Seth Vidal <skvidal@phy.duke.edu>
- enable caching option
- 0.4.3

* Tue Jan 18 2005 Seth Vidal <skvidal@phy.duke.edu>
- add man page

* Mon Jan 17 2005 Seth Vidal <skvidal@phy.duke.edu>
- 0.4.2


* Thu Oct 21 2004 Seth Vidal <skvidal@phy.duke.edu>
- ghost files not being added into primary file list if
  matching regex
- 0.4.1


* Mon Oct 11 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.4.0

* Thu Sep 30 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.3.9
- fix for groups checksum creation

* Sat Sep 11 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.3.8

* Wed Sep  1 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.3.7

* Fri Jul 23 2004 Seth Vidal <skvidal@phy.duke.edu>
- make filelists right <sigh>


* Fri Jul 23 2004 Seth Vidal <skvidal@phy.duke.edu>
- fix for broken filelists

* Mon Jul 19 2004 Seth Vidal <skvidal@phy.duke.edu>
- re-enable groups
- update num to 0.3.4

* Tue Jun  8 2004 Seth Vidal <skvidal@phy.duke.edu>
- update to the format
- versioned deps
- package counts
- uncompressed checksum in repomd.xml


* Fri Apr 16 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.3.2 - small addition of -p flag

* Sun Jan 18 2004 Seth Vidal <skvidal@phy.duke.edu>
- I'm an idiot

* Sun Jan 18 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.3

* Tue Jan 13 2004 Seth Vidal <skvidal@phy.duke.edu>
- 0.2 -

* Sat Jan 10 2004 Seth Vidal <skvidal@phy.duke.edu>
- first packaging

