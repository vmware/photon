Summary:        Fast distributed version control system
Name:           git
Version:        2.17.1
Release:        3%{?dist}
License:        GPLv2
URL:            http://git-scm.com/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
%define sha1    git=cdc8ba409643f6fe19b1bf0653d60f3aac0485f3
BuildRequires:  curl
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  openssl-devel
Requires:       python2
Requires:       openssl
Requires:       curl
Requires:       expat
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
%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
%{_datadir}/perl5/*
%{_libexecdir}/git-core/*
%{_datarootdir}/git-core/*
%{_datarootdir}/git-gui/*
%{_datarootdir}/gitk/*
%{_datarootdir}/gitweb/*
#excluding git svn files
%exclude %{_libexecdir}/git-core/*svn*
%exclude %{_mandir}/man3/*:SVN:*
%exclude %{_datadir}/perl5/Git/SVN
%exclude %{_datadir}/perl5/Git/SVN.pm
%exclude /usr/lib/perl5/5.24.1/x86_64-linux-thread-multi/perllocal.pod

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 2.17.1-3
-   Bumped up to use latest openssl
*   Wed Jun 06 2018 Xiaolin Li <xiaolinl@vmware.com> 2.17.1-2
-   Bump release after upgraded perl to 5.24.1
*   Thu May 31 2018 Xiaolin Li <xiaolinl@vmware.com> 2.17.1-1
-   Updated to version 2.17.1, fix CVE-2018-11235, CVE-2018-11233
*   Tue Apr 24 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.17.0-1
-   Updated to version 2.17.0, fix CVE-2018-1000021, CVE-2018-1000110
*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.14.2-1
-   Updated to version 2.14.2, fix CVE-2017-14867
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
-   Initial build.  First version
