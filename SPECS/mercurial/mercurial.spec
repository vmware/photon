Summary:        A free, distributed source control management tool.
Name:           mercurial
Version:        3.7.1
Release:        7%{?dist}
License:        GPLv2+
URL:            https://www.ruby-lang.org/en/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
%define sha1    mercurial=8ce55b297c6a62e987657498746eeca870301ffb
Patch0:         hg-CVE-2016-3068.patch
Patch1:         hg-CVE-2016-3069-1.patch
Patch2:         hg-CVE-2016-3069-2.patch
Patch3:         hg-CVE-2016-3069-3.patch
Patch4:         hg-CVE-2016-3069-4.patch
Patch5:         hg-CVE-2016-3069-5.patch
Patch6:         hg-CVE-2016-3105.patch
Patch7:         hg-CVE-2017-9462.patch
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
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-7
-   Fix CVE-2017-9462 patch.
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-6
-   Apply CVE-2017-9462 patch
*   Mon Jan 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-5
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
