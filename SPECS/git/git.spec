Summary:        Fast distributed version control system
Name:           git
Version:        2.14.2
Release:        3%{?dist}
License:        GPLv2
URL:            http://git-scm.com/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
%define sha1    git=9515fd4a068027f2c3d6ea9b8a8a298e990123a0
BuildRequires:  curl-devel
BuildRequires:  python2
Requires:       openssl
Requires:       curl
Requires:       expat
Requires:       perl >= 5.28.0
Requires:       perl-YAML
Requires:       perl-DBI
Requires:       perl-CGI

%description
Git is a free and open source, distributed version control system 
designed to handle everything from small to very large projects with
speed and efficiency. Every Git clone is a full-fledged repository 
with complete history and full revision tracking capabilities, not 
dependent on network access or a central server. Branching and 
merging are fast and easy to do. Git is used for version control of
files, much like tools such as Mercurial, Bazaar, 
Subversion-1.7.8, CVS-1.11.23, Perforce, and Team Foundation Server.

%package lang
Summary: Additional language files for git
Group: System Environment/Programming
Requires: git >= 2.1.2
%description lang
These are the additional language files of git.

%prep
%setup -q
%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --libexec=%{_libexecdir} \
    --with-gitconfig=/etc/gitconfig
make %{?_smp_mflags} CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/usr/share/bash-completion/completions
install -m 0644 contrib/completion/git-completion.bash %{buildroot}/usr/share/bash-completion/completions/git
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
# git expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make %{?_smp_mflags} test

%post
if [ $1 -eq 1 ];then
    # This is first installation.
    git config --system http.sslCAPath /etc/ssl/certs
    exit 0
fi

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/perl5/*
%{_libexecdir}/git-core/*
%{_mandir}/man3/*
%{_datarootdir}/git-core/*
%{_datarootdir}/git-gui/*
%{_datarootdir}/gitk/*
%{_datarootdir}/gitweb/*
%{_datarootdir}/bash-completion/
#excluding git svn files
%exclude %{_libexecdir}/git-core/*svn*
%exclude %{_mandir}/man3/*:SVN:*
%exclude %{perl_sitelib}/Git/SVN
%exclude %{perl_sitelib}/Git/SVN.pm
%exclude /usr/lib/perl5/*/*/perllocal.pod

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.14.2-3
-   Consuming perl version upgrade of 5.28.0
*   Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> 2.14.2-2
-   Excluded the perllocal.pod for aarch64.
*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.14.2-1
-   Updated to version 2.14.2, fix CVE-2017-14867
*   Mon Aug 21 2017 Rui Gu <ruig@vmware.com> 2.9.3-4
-   Fix make check with non-root mode.
*   Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.3-3
-   Remove python2 from requires.
*   Tue Apr 17 2017 Robert Qi <qij@vmware.com> 2.9.3-2
-   Update since perl version got updated.
*   Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.9.3-1
-   Updated to version 2.9.3
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.8.1-7
-   BuildRequires curl-devel.
*   Fri Aug 19 2016 Alexey Makhalov <amakhalov@vmware.com> 2.8.1-6
-   Add bash completion file
*   Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.8.1-5
-   Excluded the perllocal.pod log.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.1-4
-   GA - Bump release of all rpms
*   Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.1-3
-   Fix if syntax
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.8.1-2
-   Handling the upgrade scenario.
*   Fri Apr 15 2016 Anish Swaminathan <anishs@vmware.com> 2.8.1-1
-   Updated to version 2.8.1
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.7.1-1
-   Updated to version 2.7.1
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.1.2-2
-   Add requires for perl-CGI.
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.2-1
-   Initial build. First version
