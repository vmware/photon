Summary: 	Extra tools for rpm-ostree
Name: 		rpm-ostree-toolbox
Version: 	2016.4
Release: 	2%{?dist}
#VCS: https://github.com/cgwalters/rpm-ostree-toolbox
# This tarball is generated via "make -C packaging -f Makefile.dist-packaging dist-snapshot"
# which is really just a wrapper for "git archive".
# It doesn't follow the Github guidelines because they only work for
# github; the infrastructure above is generic for any git repository.
Source0:	%{name}-%{version}.tar.gz
%define sha1 rpm-ostree-toolbox=2c60816e5ea2ab56dcc9008018c7bbdc5d7540d0
License: 	LGPLv2+
URL: 		https://github.com/cgwalters/rpm-ostree-toolbox
Vendor:		VMware, Inc.
Distribution:	Photon
# We always run autogen.sh
BuildRequires:	autoconf automake libtool
# For docs
BuildRequires: 	gtk-doc
# BuildRequires: gnome-common
BuildRequires: 	ostree-devel
BuildRequires: 	libgsystem-devel
BuildRequires: 	json-glib-devel
BuildRequires:	which
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	gobject-introspection-devel
BuildRequires:	gobject-introspection-python
BuildRequires:  autogen
Requires: 	systemd
Requires: 	perl
Requires:	libgsystem
Requires:	gobject-introspection
Requires:	python2
Requires:	shadow
Requires:	perl-Config-IniFiles
Requires:	perl-JSON-XS

%description
Various utilities and scripts for working with rpm-ostree based
operating systems, particularly as virtual machines.

%prep
%setup -q -n %{name}-%{version}

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"

%check
make  %{?_smp_mflags} check

%pre
getent group rpmostreecompose >/dev/null || groupadd -r rpmostreecompose
getent passwd rpmostreecompose >/dev/null || \
  useradd -r -g rpmostreecompose -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -c "RPM OStree Toolbox user" rpmostreecompose

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ] ; then
    if getent passwd rpmostreecompose >/dev/null; then
        userdel rpmostreecompose
    fi
    if getent group rpmostreecompose >/dev/null; then
        groupdel rpmostreecompose
    fi
fi

%files
%doc COPYING README.md src/py/config.ini.sample
%{_bindir}/rpm-ostree-toolbox
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.gz

%dir %{_localstatedir}/lib/%{name}
%attr(0755,rpmostreecompose,rpmostreecompose) %{_localstatedir}/lib/%{name}

%changelog
*   Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2016.4-2
-	Created libgsystem-devel & updated build requires
*   Wed Apr 12 2017 Siju Maliakkal <smaliakkal@vmware.com> 2016.4-1
-   Updated to latest version   
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2015.12-4
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.12-3
-	GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 2015.12-2
-   Clean up the spec file.
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 2015.12-1
-   Updated to version 2015.12
*   Sat May 24 2014 Colin Walters <walters@verbum.org> - 2014.11-1
-   Initial package

