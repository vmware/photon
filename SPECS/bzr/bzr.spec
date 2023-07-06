%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A version control system
Name:           bzr
Version:        2.7.0
Release:        3%{?dist}
License:        GPLv2+
URL:            http://www.bazaar-vcs.org/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://launchpad.net/bzr/2.7/2.7.0/+download/bzr-2.7.0.tar.gz
%define sha512  bzr=c39ad3715d865788da74d8de8b469e1dc93d18b6cbcbc569464cdeb9bb2173bf8d7f4f8ee8f7599fbcbbe322817a4c72e785d544e622753699c425c32597d9aa
BuildRequires:  python2-devel
Patch0:         CVE-2017-14176.patch

%description
Bazaar is a version control system that helps you track project history over time and to collaborate easily with others. Whether you're a single developer, a co-located team or a community of developers scattered across the world, Bazaar scales and adapts to meet your needs. Part of the GNU Project, Bazaar is free software sponsored by Canonical. For a closer look, see ten reasons to switch to Bazaar.

%prep
%autosetup -p1
%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-data=/usr/share
%{find_lang} bzr

%check
python2 setup.py check

%files -f bzr.lang
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/bzr
%{_mandir}/man1/*

%changelog
*   Thu Jul 06 2023 Anmol Jain <anmolja@vmware.com> 2.7.0-3
-   Fix for CVE-2017-14176
*   Tue Jan 07 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.7.0-2
-   Added python2-devel as a build requirement
*   Thu Jun 22 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build. First version
