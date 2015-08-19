Summary: 	Extra tools for rpm-ostree
Name: 		rpm-ostree-toolbox
Version: 	2015.3
Release: 	1%{?dist}
#VCS: https://github.com/cgwalters/rpm-ostree-toolbox
# This tarball is generated via "make -C packaging -f Makefile.dist-packaging dist-snapshot"
# which is really just a wrapper for "git archive".
# It doesn't follow the Github guidelines because they only work for
# github; the infrastructure above is generic for any git repository.
Source0:	%{name}-%{version}.tar.gz
%define sha1 rpm-ostree-toolbox=bd8e4b5da029990845233bceac765322c62db848
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
BuildRequires: 	libgsystem
BuildRequires: 	json-glib-devel
BuildRequires:	which
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	gobject-introspection-devel
BuildRequires:	gobject-introspection-python
Requires: 	systemd
Requires: 	perl
Requires:	gobject-introspection
Requires:	python2
Requires:	shadow
Requires:	perl-Config-IniFiles
Requires:	perl-JSON-XS
# 
# %global unprivileged_user rpmostreecompose
# %global unprivileged_group rpmostreecompose
# 
# Requires: python
# Requires: python-iniparse
# Requires: pygobject2
# Requires: gjs
# Requires: libvirt-python
# Requires: libguestfs-tools-c
# Requires: libguestfs-gobject
# # Needed for libguests
# Requires: kernel
# 
# Requires: rpm-ostree
# Requires: lorax
# 
# %if 0%{?fedora}
# Requires: docker-io
# %else
# Requires: docker
# %endif
# 
# # Imagefactory
# Requires: imagefactory >= 1.1.7-1
# Requires: imagefactory-plugins-TinMan >= 1.1.7-1
# Requires: imagefactory-plugins-OVA >= 1.1.7-1
# Requires: imagefactory-plugins-vSphere >= 1.1.7-1
# Requires: imagefactory-plugins-RHEVM >= 1.1.7-1
# Requires: imagefactory-plugins-IndirectionCloud >= 1.1.7-1
# 
# Requires: VMDKstream >= 0.3-1
# 
# %if 0%{?rhel}
# %else
# Requires: libguestfs-xfs
# %endif
# # Needed for rpmostree-build-monitor
# Requires:       python-qpid
# Requires:       cyrus-sasl-gssapi
# Requires:       python-saslwrapper
# Requires(pre):  shadow-utils
# Requires:       systemd-units
# Requires(post): systemd-units

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

%pre
getent group %{unprivileged_group} >/dev/null || groupadd -r %{unprivileged_group}
getent passwd %{unprivileged_user} >/dev/null || \
  useradd -r -g %{unprivileged_group} -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -c "RPM OStree Toolbox user" %{unprivileged_user}

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%doc COPYING README.md src/py/config.ini.sample
%{_bindir}/rpm-ostree-toolbox
%{_bindir}/rpm-ostree-toolbox-kinit
%{_bindir}/rpm-ostree-toolbox-build-monitor
%{_bindir}/rpm-ostree-toolbox-git-monitor
%{_bindir}/rpm-ostree-toolbox-watch
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.gz

%dir %{_localstatedir}/lib/%{name}
%attr(0755,%{unprivileged_user},%{unprivileged_group}) %{_localstatedir}/lib/%{name}

%config %{_sysconfdir}/sysconfig/%{name}-template

/usr/lib/systemd/system/rpm-ostree-toolbox-build-monitor@.service
/usr/lib/systemd/system/rpm-ostree-toolbox-git-monitor.service
/usr/lib/systemd/system/rpm-ostree-toolbox-kinit@.service
/usr/lib/systemd/system/rpm-ostree-toolbox-kinit@.timer
/usr/lib/systemd/system/rpm-ostree-toolbox-watch@.service


%changelog
* Sat May 24 2014 Colin Walters <walters@verbum.org> - 2014.11-1
- Initial package

