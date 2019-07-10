Summary:        A free, distributed source control management tool.
Name:           mercurial
Version:        4.5.3
Release:        3%{?dist}
License:        GPLv2+
URL:            https://www.mercurial-scm.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.mercurial-scm.org/release/%{name}-%{version}.tar.gz
%define sha1    mercurial=465216f1fabc571a8de731531e2aa0aa12833e56
Patch0:         mercurial-disable-zstd.patch
Patch1:         mercurial-fix-CVE-2018-17983.patch
Patch2:         mercurial-fix-CVE-2018-13347.patch
Patch3:         mercurial-fix-CVE-2018-13346.patch
Patch4:         mercurial-fix-CVE-2018-13348.patch
Patch5:         mercurial-fix-CVE-2019-3902_1.patch
Patch6:         mercurial-fix-CVE-2019-3902_2.patch
Patch7:         mercurial-fix-CVE-2019-3902_3.patch
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       python2
%description
Mercurial is a distributed source control management tool similar to Git and Bazaar.
Mercurial is written in Python and is used by projects such as Mozilla and Vim.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
make build
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{_bindir}
%{__python} setup.py install --skip-build --root %{buildroot}

cat >> %{buildroot}/.hgrc << "EOF"
[ui]
username = "$(id -u)"
EOF

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
/.hgrc
%{_bindir}/hg
%{python_sitelib}/*

%changelog
*   Thu May 16 2019 Keerthana K <keerthanak@vmware.com> 4.5.3-3
-   Fix CVE-2019-3902
*   Mon May 06 2019 Keerthana K <keerthanak@vmware.com> 4.5.3-2
-   Fix CVE-2018-17983, CVE-2018-13346, CVE-2018-13347, CVE-2018-13348
*   Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 4.5.3-1
-   Update version to 4.5.3 for CVE-2018-1000132
*   Tue Nov 14 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-2
-   Disable zstd.
*   Tue Oct 17 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
-   Update verion to 4.3.3 for CVE-2017-1000115, CVE-2017-1000116.
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-7
-   Fix CVE-2017-9462 patch.
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-6
-   Apply CVE-2017-9462 patch
*   Sun Jan 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-5
-   Install with setup.py.
*   Tue Nov 22 2016 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-4
-   Apply patches for CVE-2016-3068, CVE-2016-3069, CVE-2016-3105
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.7.1-3
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.7.1-2
-   Edit postun script.
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.7.1-1
-   Updating Version.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.1.2-4
-   Edit post script.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.1.2-3
-   Change path to /var/opt.
*   Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
-   /etc/profile.d permission fix
*   Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-   Initial build.  First version
