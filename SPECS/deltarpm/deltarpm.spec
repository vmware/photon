Summary: Create deltas between rpms
Name: deltarpm
Version: 3.6.1
Release: 1%{?dist}
License: BSD
Group: Applications/System
Vendor: VMware, Inc.
Distribution: Photon
URL: https://github.com/rpm-software-management/deltarpm
Source0: https://github.com/rpm-software-management/deltarpm/archive/deltarpm-%{version}.tar.gz
%define sha1 deltarpm=29f39a8c55f48a7e538cabe49ca3203ebb823b2c
BuildRequires: rpm-devel >= 4.2
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: popt-devel
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
Requires: perl
Requires: python2
Requires: python2-libs


%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%prep
%setup

%build
%{__make} %{?_smp_mflags} prefix="%{_prefix}" mandir="%{_mandir}"
%{__make} %{?_smp_mflags} prefix="%{_prefix}" mandir="%{_mandir}" python

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" prefix="%{_prefix}" mandir="%{_mandir}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltaiso.8*
%doc %{_mandir}/man8/applydeltarpm.8*
%doc %{_mandir}/man8/combinedeltarpm.8*
%doc %{_mandir}/man8/drpmsync.8*
%doc %{_mandir}/man8/makedeltaiso.8*
%doc %{_mandir}/man8/makedeltarpm.8*
%doc %{_mandir}/man8/fragiso.8*
%{_bindir}/applydeltaiso
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/drpmsync
%{_bindir}/makedeltaiso
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader
%{_bindir}/fragiso
%{python_sitelib}/*

%changelog
* Tue Apr 25 2017 Bo Gan <ganb@vmware.com> 3.6.1-1
- Update to 3.6.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6-2
-	GA - Bump release of all rpms
* Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> - 3.6-2
- Fixed Python install.

* Fri Mar 09 2007 Dag Wieers <dag@wieers.com> - 3.3-2
- Fixed group.

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1
- Initial package.
