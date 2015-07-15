Summary:	Mercurial-3.1.2
Name:		mercurial
Version:	3.1.2
Release:	2%{?dist}
License:	GPLv2+
URL:		https://www.ruby-lang.org/en/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
%define sha1 mercurial=ae7e16454cee505da895c2497f09711f35287459
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

install -vdm755 %{buildroot}/opt/%{name}-%{version}
mv -v %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/%{name}-%{version}/
chown -R root:root %{buildroot}/opt/%{name}-%{version}

install -vdm755 %{buildroot}/bin
ln -sfv ../opt/%{name}-%{version}/hg %{buildroot}/bin/hg
cat >> %{buildroot}/.hgrc << "EOF"
[ui]
username = "$(id -u)"
EOF

install -vdm755 %{buildroot}/etc/profile.d
cat >> %{buildroot}/etc/profile.d/mercurial-exports.sh <<- "EOF"
export PYTHONPATH="$PYTHONPATH:/opt/%{name}-%{version}/mercurial/pure"
EOF

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
rm /etc/profile.d/java-exports.sh
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/.hgrc
/opt/%{name}-%{version}/*
/bin/hg
/etc/profile.d/mercurial-exports.sh
%exclude /opt/%{name}-%{version}/contrib/plan9
%exclude /opt/%{name}-%{version}/build/temp.*
%changelog
*	Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
-	/etc/profile.d permission fix
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-	Initial build.	First version
