%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:    A free, distributed source control management tool.
Name:       mercurial
Version:    4.1
Release:    3%{?dist}
License:    GPLv2+
URL:        https://www.ruby-lang.org/en/
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
%define sha1 mercurial=d5f88e05cbbd8f13dd5fc4004433f54435fc27c8
Patch0:         hg-CVE-2017-9462.patch
BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
Requires:      python2

%description
Mercurial is a distributed source control management tool similar to Git and Bazaar.
Mercurial is written in Python and is used by projects such as Mozilla and Vim.

%prep
%setup -q
%patch0 -p1

%build
make build

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{_bindir}
python2 setup.py install --skip-build --root %{buildroot}

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
%defattr(-,root,root)
/.hgrc
%{_bindir}/hg
%{python2_sitelib}/*

%changelog
*   Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1-3
-   Use python2 explicitly while building
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.1-2
-   Apply CVE-2017-9462 patch
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.1-1
-   Update package version
*   Mon Jan 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-6
-   Install with setup.py.
*   Tue Nov 22 2016 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-5
-   Apply patches for CVE-2016-3068, CVE-2016-3069, CVE-2016-3105
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.7.1-4
-   Modified %check
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
