%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A version control system
Name:           bzr
Version:        2.7.0
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.bazaar-vcs.org/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://launchpad.net/bzr/2.7/2.7.0/+download/bzr-2.7.0.tar.gz
%define sha1    bzr=872f6088f8b07558519dbbc88fffa05e37602f52
BuildRequires:  python2

%description
Bazaar is a version control system that helps you track project history over time and to collaborate easily with others. Whether you're a single developer, a co-located team or a community of developers scattered across the world, Bazaar scales and adapts to meet your needs. Part of the GNU Project, Bazaar is free software sponsored by Canonical. For a closer look, see ten reasons to switch to Bazaar.

%prep
%setup -q

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
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.7.0-2
-   Added BuildRequires python2
*   Thu Jun 22 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build. First version
