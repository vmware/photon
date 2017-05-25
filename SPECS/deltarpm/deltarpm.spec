%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Create deltas between rpms
Name:           deltarpm
Version:        3.6.1
Release:        2%{?dist}
License:        BSD
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://github.com/rpm-software-management/deltarpm
Source0: https://github.com/rpm-software-management/deltarpm/archive/deltarpm-%{version}.tar.gz
%define sha1 deltarpm=29f39a8c55f48a7e538cabe49ca3203ebb823b2c
BuildRequires:  rpm-devel >= 4.2
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  popt-devel
Requires:       perl

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package        python
Summary:        Python2 bindings for deltarpm
License:        LGPLv2+
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       %{name} = %{version}-%{release}
Requires:       python2

%description python
The deltarpm-python package contains the python2 bindings for deltarpm.

%package  -n    python3-deltarpm
Summary:        Python3 bindings for deltarpm
License:        LGPLv2+
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       %{name} = %{version}-%{release}
Requires:       python2

%description -n python3-deltarpm
The python3-deltarpm package contains the python3 bindings for deltarpm.
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

%files python
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-deltarpm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-2
-   Move python2 requires to python subpackage and added python3.
*   Tue Apr 25 2017 Bo Gan <ganb@vmware.com> 3.6.1-1
-   Update to 3.6.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6-2
-   GA - Bump release of all rpms
*   Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> - 3.6-2
-   Fixed Python install.

*   Fri Mar 09 2007 Dag Wieers <dag@wieers.com> - 3.3-2
-   Fixed group.

*   Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1
-   Initial package.
