Summary:	Mercurial-3.1.2
Name:		mercurial
Version:	3.7.1
Release:	3%{?dist}
License:	GPLv2+
URL:		https://www.ruby-lang.org/en/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
%define sha1 mercurial=8ce55b297c6a62e987657498746eeca870301ffb
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Requires:	python2
%description
Mercurial is a distributed source control management tool similar to Git and Bazaar.
Mercurial is written in Python and is used by projects such as Mozilla and Vim.

%prep
%setup -q
%build
make build
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make PREFIX=%{_prefix} install-bin

install -vdm755 %{buildroot}/var/opt/%{name}-%{version}
mv -v %{_builddir}/%{name}-%{version}/* %{buildroot}/var/opt/%{name}-%{version}/
chown -R root:root %{buildroot}/var/opt/%{name}-%{version}

install -vdm755 %{buildroot}/bin
ln -sfv ../var/opt/%{name}-%{version}/hg %{buildroot}/bin/hg
cat >> %{buildroot}/.hgrc << "EOF"
[ui]
username = "$(id -u)"
EOF

install -vdm755 %{buildroot}/etc/profile.d
cat >> %{buildroot}/etc/profile.d/mercurial-exports.sh <<- "EOF"
export PYTHONPATH="$PYTHONPATH:/var/opt/%{name}-%{version}/mercurial/pure"
EOF

%{_fixperms} %{buildroot}/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/.hgrc
/var/opt/%{name}-%{version}/*
/bin/hg
/etc/profile.d/mercurial-exports.sh
%exclude /var/opt/%{name}-%{version}/contrib/plan9
%exclude /var/opt/%{name}-%{version}/build/temp.*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.7.1-3
-	GA - Bump release of all rpms
*	Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.7.1-2
-	Edit postun script.
*       Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.7.1-1
-       Updating Version.
*	Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.1.2-4
-	Edit post script.
*	Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.1.2-3
-	Change path to /var/opt.
*	Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
-	/etc/profile.d permission fix
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-	Initial build.	First version
