Summary:	Fast distributed version control system
Name:		git
Version:	2.1.2
Release:	1%{?dist}
License:	GPLv2
URL:		http://git-scm.com/
Group:		System Environment/Programming
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
%define sha1 git=b0d38bf2161286f2039a9a2adb4c8f7e5308e824
BuildRequires:  curl
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	openssl-devel
Requires:	python2
Requires:	openssl
Requires:	curl
Requires:	expat
Requires:	perl-YAML
Requires:	perl-DBI

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
git config --system http.sslCAPath /etc/ssl/certs
exit 0
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
#excluding git svn files
%exclude %{_libexecdir}/git-core/*svn*
%exclude %{_mandir}/man3/*:SVN:*
%exclude %{perl_sitelib}/Git/SVN
%exclude %{perl_sitelib}/Git/SVN.pm

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.2-1
-	Initial build.	First version
