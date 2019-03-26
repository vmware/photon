%global debug_package %{nil}
%bcond_with lowmem_builder
%{!?_udevrulesdir: %define _udevrulesdir /lib/udev/rules.d}
%{!?tmpfiles_create: %define tmpfiles_create systemd-tmpfiles --create}

%define python3_pkgversion 3
%define tmpfiles_create systemd-tmpfiles --create
%define _udevrulesdir /lib/udev/rules.d
%define _libexecdir %{_exec_prefix}/lib
%define _unitdir /usr/lib/systemd/system

#################################################################################
# common
#################################################################################
Name:       ceph
Version:    12.2.4
Release:    3%{?dist}
Epoch:      1
Summary:    User space components of the Ceph file system
License:    LGPL-2.1 and CC-BY-SA-1.0 and GPL-2.0 and BSL-1.0 and GPL-2.0-with-autoconf-exception and BSD-3-Clause and MIT
Group:      System/Filesystems
URL:        http://ceph.com/
Source0:    http://ceph.com/download/%{name}-%{version}.tar.gz
%define sha1 ceph=df93bc3fac55249f5f0d30caa567962b387693dd
Vendor:     VMware, Inc.
Distribution:   Photon
Patch0:     CVE-2018-10861.patch
Patch1:     build_fix_CVE-2018-10861.patch
Patch2:     CVE-2018-16889.patch
#################################################################################
# dependencies that apply across all distro families
#################################################################################
Requires:       ceph-osd = %{epoch}:%{version}-%{release}
Requires:       ceph-mds = %{epoch}:%{version}-%{release}
Requires:       ceph-mgr = %{epoch}:%{version}-%{release}
Requires:       ceph-mon = %{epoch}:%{version}-%{release}
Requires(post): binutils
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  fuse-devel
BuildRequires:  gdbm-devel
BuildRequires:  leveldb-devel > 1.2
BuildRequires:  libaio-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  systemd-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  parted
BuildRequires:  perl
BuildRequires:  pkg-config
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python-xml
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python-requests
BuildRequires:  python-sphinx
BuildRequires:  snappy-devel
BuildRequires:  (util-linux or toybox)
BuildRequires:  valgrind
BuildRequires:  xfsprogs
BuildRequires:  xfsprogs-devel
BuildRequires:  nasm

#################################################################################
# distro-conditional dependencies
#################################################################################
Requires:   systemd
BuildRequires:  boost
BuildRequires:  btrfs-progs
BuildRequires:  nss-devel
BuildRequires:  keyutils-devel
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  cython
BuildRequires:  cython3
BuildRequires:  python-setuptools
BuildRequires:  fcgi-devel
BuildRequires:  gperf


%description
Ceph is a massively scalable, open-source, distributed storage system that runs
on commodity hardware and delivers object, block and file system storage.


#################################################################################
# packages
#################################################################################
%package base
Summary:       Ceph Base Package
Group:         System Environment/Base
Requires:      ceph-common = %{epoch}:%{version}-%{release}
Requires:      librbd1 = %{epoch}:%{version}-%{release}
Requires:      librados2 = %{epoch}:%{version}-%{release}
Requires:      libcephfs2 = %{epoch}:%{version}-%{release}
Requires:      librgw2 = %{epoch}:%{version}-%{release}

Requires:      python2
Requires:      python-requests
Requires:      python-setuptools
Requires:      /bin/grep
Requires:      xfsprogs
Requires:      logrotate
Requires:      (util-linux or toybox)
Requires:      (findutils or toybox)
Requires:      /usr/bin/which
%description base
Base is the package that includes all the files shared amongst ceph servers

%package -n ceph-common
Summary:    Ceph Common
Group:      System Environment/Base
Requires:   librbd1 = %{epoch}:%{version}-%{release}
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   libcephfs2 = %{epoch}:%{version}-%{release}
Requires:   python-rados = %{epoch}:%{version}-%{release}
Requires:   python-rbd = %{epoch}:%{version}-%{release}
Requires:   python-cephfs = %{epoch}:%{version}-%{release}
Requires:   python-rgw = %{epoch}:%{version}-%{release}
Requires:   python-requests
%{?systemd_requires}
%description -n ceph-common
Common utilities to mount and interact with a ceph storage cluster.
Comprised of files that are common to Ceph clients and servers.

%package mds
Summary:    Ceph Metadata Server Daemon
Group:      System Environment/Base
Requires:   ceph-base = %{epoch}:%{version}-%{release}
%description mds
ceph-mds is the metadata server daemon for the Ceph distributed file system.
One or more instances of ceph-mds collectively manage the file system
namespace, coordinating access to the shared OSD cluster.

%package mon
Summary:    Ceph Monitor Daemon
Group:      System Environment/Base
Requires:   ceph-base = %{epoch}:%{version}-%{release}
%description mon
ceph-mon is the cluster monitor daemon for the Ceph distributed file
system. One or more instances of ceph-mon form a Paxos part-time
parliament cluster that provides extremely reliable and durable storage
of cluster membership, configuration, and state.

%package mgr
Summary:        Ceph Manager Daemon
License:        LGPL-2.1 and CC-BY-SA-1.0 and GPL-2.0 and BSL-1.0 and GPL-2.0-with-autoconf-exception and BSD-3-Clause and MIT
Group:          System Environment/Base
Requires:       ceph-base = %{epoch}:%{version}-%{release}

%description mgr
ceph-mgr enables python modules that provide services (such as the REST
module derived from Calamari) and expose CLI hooks.  ceph-mgr gathers
the cluster maps, the daemon metadata, and performance counters, and
exposes all these to the python modules.

%package fuse
Summary:    Ceph fuse-based client
Group:      System Environment/Base
%description fuse
FUSE based client for Ceph distributed network file system

%package -n rbd-fuse
Summary:    Ceph fuse-based client
Group:      System Environment/Base
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   librbd1 = %{epoch}:%{version}-%{release}
%description -n rbd-fuse
FUSE based client to map Ceph rbd images to files

%package -n rbd-mirror
Summary:    Ceph daemon for mirroring RBD images
Group:      System Environment/Base
Requires:   ceph-common = %{epoch}:%{version}-%{release}
Requires:   librados2 = %{epoch}:%{version}-%{release}
%description -n rbd-mirror
Daemon for mirroring RBD images between Ceph clusters, streaming
changes asynchronously.

%package -n rbd-nbd
Summary:    Ceph RBD client base on NBD
Group:      System Environment/Base
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   librbd1 = %{epoch}:%{version}-%{release}
%description -n rbd-nbd
NBD based client to map Ceph rbd images to local device

%package radosgw
Summary:    Rados REST gateway
Group:      Development/Libraries
Requires:   ceph-common = %{epoch}:%{version}-%{release}
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   librgw2 = %{epoch}:%{version}-%{release}
%description radosgw
RADOS is a distributed object store used by the Ceph distributed
storage system.  This package provides a REST gateway to the
object store that aims to implement a superset of Amazon's S3
service as well as the OpenStack Object Storage ("Swift") API.

%package osd
Summary:    Ceph Object Storage Daemon
Group:      System Environment/Base
Requires:   ceph-base = %{epoch}:%{version}-%{release}
Requires:   gptfdisk
Requires:       parted
%description osd
ceph-osd is the object storage daemon for the Ceph distributed file
system.  It is responsible for storing objects on a local file system
and providing access to them over the network.

%package -n librados2
Summary:    RADOS distributed object store client library
Group:      System Environment/Libraries
License:    LGPL-2.0
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:  ceph-libs < %{epoch}:%{version}-%{release}
Requires:   libatomic_ops
Requires:   libceph-common = %{epoch}:%{version}-%{release}
%endif
%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librados-devel
Summary:    RADOS headers
Group:      Development/Libraries
License:    LGPL-2.0
Requires:   librados2 = %{epoch}:%{version}-%{release}
Obsoletes:  ceph-devel < %{epoch}:%{version}-%{release}
Provides:   librados2-devel = %{epoch}:%{version}-%{release}
Obsoletes:  librados2-devel < %{epoch}:%{version}-%{release}
%description -n librados-devel
This package contains libraries and headers needed to develop programs
that use RADOS object store.

%package -n librgw2
Summary:    RADOS gateway client library
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   libceph-common = %{epoch}:%{version}-%{release}
%description -n librgw2
This package provides a library implementation of the RADOS gateway
(distributed object store with S3 and Swift personalities).

%package -n librgw-devel
Summary:    RADOS gateway client library
Group:      Development/Libraries
License:    LGPL-2.0
Requires:   librados-devel = %{epoch}:%{version}-%{release}
Requires:   librgw2 = %{epoch}:%{version}-%{release}
Provides:   librgw2-devel = %{epoch}:%{version}-%{release}
Obsoletes:  librgw2-devel < %{epoch}:%{version}-%{release}
%description -n librgw-devel
This package contains libraries and headers needed to develop programs
that use RADOS gateway client library.

%package -n python-rgw
Summary:    Python 2 libraries for the RADOS gateway
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librgw2 = %{epoch}:%{version}-%{release}
Requires:   python-rados = %{epoch}:%{version}-%{release}
Obsoletes:  python-ceph < %{epoch}:%{version}-%{release}
%description -n python-rgw
This package contains Python 2 libraries for interacting with Cephs RADOS
gateway.

%package -n python3-rgw
Summary:    Python 3 libraries for the RADOS gateway
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librgw2 = %{epoch}:%{version}-%{release}
Requires:   python3-rados = %{epoch}:%{version}-%{release}
%description -n python3-rgw
This package contains Python 3 libraries for interacting with Cephs RADOS
gateway.

%package -n python-rados
Summary:    Python 2 libraries for the RADOS object store
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librados2 = %{epoch}:%{version}-%{release}
Obsoletes:  python-ceph < %{epoch}:%{version}-%{release}
%description -n python-rados
This package contains Python 2 libraries for interacting with Cephs RADOS
object store.

%package -n python3-rados
Summary:    Python 3 libraries for the RADOS object store
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   python3
Requires:   librados2 = %{epoch}:%{version}-%{release}
%description -n python3-rados
This package contains Python 3 libraries for interacting with Cephs RADOS
object store.

%package -n libceph-common
Summary:    libceph-common
Group:      System Environment/Libraries
License:    LGPL-2.0
%description -n libceph-common
libceph-common.

%package -n libradosstriper1
Summary:    RADOS striping interface
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librados2 = %{epoch}:%{version}-%{release}
Requires:   libceph-common = %{epoch}:%{version}-%{release}
%description -n libradosstriper1
Striping interface built on top of the rados library, allowing
to stripe bigger objects onto several standard rados objects using
an interface very similar to the rados one.

%package -n libradosstriper-devel
Summary:    RADOS striping interface headers
Group:      Development/Libraries
License:    LGPL-2.0
Requires:   libradosstriper1 = %{epoch}:%{version}-%{release}
Requires:   librados-devel = %{epoch}:%{version}-%{release}
Obsoletes:  ceph-devel < %{epoch}:%{version}-%{release}
Provides:   libradosstriper1-devel = %{epoch}:%{version}-%{release}
Obsoletes:  libradosstriper1-devel < %{epoch}:%{version}-%{release}
%description -n libradosstriper-devel
This package contains libraries and headers needed to develop programs
that use RADOS striping interface.

%package -n librbd1
Summary:    RADOS block device client library
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librados2 = %{epoch}:%{version}-%{release}
Obsoletes:  ceph-libs < %{epoch}:%{version}-%{release}
Requires:   libceph-common = %{epoch}:%{version}-%{release}

%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n librbd-devel
Summary:    RADOS block device headers
Group:      Development/Libraries
License:    LGPL-2.0
Requires:   librbd1 = %{epoch}:%{version}-%{release}
Requires:   librados-devel = %{epoch}:%{version}-%{release}
Obsoletes:  ceph-devel < %{epoch}:%{version}-%{release}
Provides:   librbd1-devel = %{epoch}:%{version}-%{release}
Obsoletes:  librbd1-devel < %{epoch}:%{version}-%{release}
%description -n librbd-devel
This package contains libraries and headers needed to develop programs
that use RADOS block device.

%package -n python-rbd
Summary:    Python 2 libraries for the RADOS block device
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librbd1 = %{epoch}:%{version}-%{release}
Requires:   python-rados = %{epoch}:%{version}-%{release}
Obsoletes:  python-ceph < %{epoch}:%{version}-%{release}
%description -n python-rbd
This package contains Python 2 libraries for interacting with Cephs RADOS
block device.

%package -n python3-rbd
Summary:    Python 3 libraries for the RADOS block device
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   librbd1 = %{epoch}:%{version}-%{release}
Requires:   python3-rados = %{epoch}:%{version}-%{release}
%description -n python3-rbd
This package contains Python 3 libraries for interacting with Cephs RADOS
block device.

%package -n libcephfs2
Summary:    Ceph distributed file system client library
Group:      System Environment/Libraries
License:    LGPL-2.0
Obsoletes:  ceph-libs < %{epoch}:%{version}-%{release}
Obsoletes:  ceph-libcephfs
Requires:   libceph-common = %{epoch}:%{version}-%{release}
%description -n libcephfs2
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n libcephfs-devel
Summary:    Ceph distributed file system headers
Group:      Development/Libraries
License:    LGPL-2.0
Requires:   libcephfs2 = %{epoch}:%{version}-%{release}
Requires:   librados-devel = %{epoch}:%{version}-%{release}
Obsoletes:  ceph-devel < %{epoch}:%{version}-%{release}
Provides:   libcephfs2-devel = %{epoch}:%{version}-%{release}
Obsoletes:  libcephfs2-devel < %{epoch}:%{version}-%{release}
%description -n libcephfs-devel
This package contains libraries and headers needed to develop programs
that use Cephs distributed file system.

%package -n python-cephfs
Summary:    Python 2 libraries for Ceph distributed file system
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   libcephfs2 = %{epoch}:%{version}-%{release}
Requires:   python-rados = %{epoch}:%{version}-%{release}
Obsoletes:  python-ceph < %{epoch}:%{version}-%{release}
%description -n python-cephfs
This package contains Python 2 libraries for interacting with Cephs distributed
file system.

%package -n python3-cephfs
Summary:    Python 3 libraries for Ceph distributed file system
Group:      System Environment/Libraries
License:    LGPL-2.0
Requires:   libcephfs2 = %{epoch}:%{version}-%{release}
Requires:   python3-rados = %{epoch}:%{version}-%{release}
%description -n python3-cephfs
This package contains Python 3 libraries for interacting with Cephs distributed
file system.

%package -n python3-ceph-argparse
Summary:    Python 3 utility libraries for Ceph CLI
Group:      System Environment/Libraries
License:    LGPL-2.0
%description -n python3-ceph-argparse
This package contains types and routines for Python 3 used by the Ceph CLI as
well as the RESTful interface. These have to do with querying the daemons for
command-description information, validating user command input against those
descriptions, and submitting the command to the appropriate daemon.

%package -n python-ceph-compat
Summary:    Compatibility package for Cephs python libraries
Group:      System Environment/Libraries
License:    LGPL-2.0
Obsoletes:  python-ceph < %{epoch}:%{version}-%{release}
Requires:   python-rados = %{epoch}:%{version}-%{release}
Requires:   python-rbd = %{epoch}:%{version}-%{release}
Requires:   python-cephfs = %{epoch}:%{version}-%{release}
Requires:   python-rgw = %{epoch}:%{version}-%{release}
Provides:   python-ceph = %{epoch}:%{version}-%{release}
%description -n python-ceph-compat
This is a compatibility package to accommodate python-ceph split into
python-rados, python-rbd, python-rgw and python-cephfs. Packages still
depending on python-ceph should be fixed to depend on python-rados,
python-rbd, python-rgw or python-cephfs instead.

#################################################################################
# common
#################################################################################
%prep
%setup -n ceph-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%if %{with lowmem_builder}
RPM_OPT_FLAGS="$RPM_OPT_FLAGS --param ggc-min-expand=20 --param ggc-min-heapsize=32768"
%endif
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/i386/i486/'`

export CPPFLAGS="$java_inc"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

env | sort

mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR=%{_localstatedir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/ceph \
    -DWITH_EMBEDDED=OFF \
    -DWITH_MANPAGE=OFF \
    -DWITH_PYTHON3=ON \
    -DWITH_SYSTEMD=ON \
    -DWITH_XIO=OFF \
    -DWITH_TESTS=OFF \
    -DWITH_LTTNG=OFF \
    -DWITH_BABELTRACE=OFF \
    $CEPH_EXTRA_CMAKE_ARGS \
    -DWITH_OCF=OFF

make %{?_smp_mflags}

%install
pushd build
make DESTDIR=%{buildroot} install
# we have dropped sysvinit bits
rm -f %{buildroot}/%{_sysconfdir}/init.d/ceph
popd
install -m 0644 -D src/etc-rbdmap %{buildroot}%{_sysconfdir}/ceph/rbdmap
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_sysconfdir}/sysconfig/ceph
install -m 0644 -D systemd/ceph.tmpfiles.d %{buildroot}%{_tmpfilesdir}/ceph-common.conf
install -m 0755 -D systemd/ceph %{buildroot}%{_sbindir}/rcceph
install -m 0644 -D systemd/50-ceph.preset %{buildroot}%{_libexecdir}/systemd/system-preset/50-ceph.preset
mkdir -p %{buildroot}%{_sbindir}
sed -i 's/\/bin/\/usr\/bin/g' %{buildroot}%{_bindir}/ceph
sed -i 's/\/bin/\/usr\/bin/g' %{buildroot}%{_bindir}/ceph-detect-init
sed -i 's/\/bin/\/usr\/bin/g' %{buildroot}%{_sbindir}/ceph-disk
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph
chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf

# udev rules
install -m 0644 -D udev/50-rbd.rules %{buildroot}%{_udevrulesdir}/50-rbd.rules
install -m 0644 -D udev/60-ceph-by-parttypeuuid.rules %{buildroot}%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
install -m 0644 -D udev/95-ceph-osd.rules %{buildroot}%{_udevrulesdir}/95-ceph-osd.rules

#set up placeholder directories
mkdir -p %{buildroot}%{_sysconfdir}/ceph
mkdir -p %{buildroot}%{_localstatedir}/run/ceph
mkdir -p %{buildroot}%{_localstatedir}/log/ceph
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mon
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/radosgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rgw

%clean
rm -rf %{buildroot}

#################################################################################
# files and systemd scriptlets
#################################################################################
%files

%files base
%defattr(-,root,root,-)
%docdir %{_docdir}
%dir %{_docdir}/ceph
%{_docdir}/ceph/sample.ceph.conf
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-run
%{_bindir}/ceph-detect-init
%{_libexecdir}/systemd/system-preset/50-ceph.preset
%{_sbindir}/ceph-create-keys
%{_sbindir}/rcceph
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/*
%dir %{_libdir}/ceph
%{_libexecdir}/ceph/ceph_common.sh
%dir %{_libdir}/ceph/erasure-code
%{_libdir}/ceph/erasure-code/libec_*.so*
%dir %{_libdir}/ceph/compressor
%{_libdir}/ceph/compressor/libceph_*.so*
%if %{with lttng}
%{_libdir}/libos_tp.so*
%{_libdir}/libosd_tp.so*
%endif
%config %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/sysconfig/ceph
%{_unitdir}/ceph.target
%{python_sitelib}/ceph_detect_init*
%{python_sitelib}/ceph_disk*
#set up placeholder directories
%attr(750,ceph,ceph) %dir %{_localstatedir}/run/ceph
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/tmp
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-osd
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mds
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rgw

%post base
/sbin/ldconfig
%systemd_post ceph.target
/usr/bin/systemctl start ceph.target >/dev/null 2>&1 || :

%preun base
%systemd_preun ceph.target

%postun base
/sbin/ldconfig
%systemd_postun ceph.target

%files common
%defattr(-,root,root,-)
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-syn
%{_bindir}/ceph-crush-location
%{_bindir}/cephfs-data-scan
%{_bindir}/cephfs-journal-tool
%{_bindir}/cephfs-table-tool
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/rbdmap
%{_bindir}/ceph-bluestore-tool
%{_sbindir}/mount.ceph
%{_sbindir}/ceph-volume
%{_sbindir}/ceph-volume-systemd
%if %{with lttng}
%{_bindir}/rbd-replay-prep
%endif
%{_bindir}/ceph-post-file
%{_bindir}/ceph-brag
%{_tmpfilesdir}/ceph-common.conf
%dir %{_datadir}/ceph/
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_unitdir}/rbdmap.service
%{_unitdir}/ceph-volume@.service
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_daemon.py*
%dir %{_udevrulesdir}
%{_udevrulesdir}/50-rbd.rules
%attr(3770,ceph,ceph) %dir %{_localstatedir}/log/ceph/
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/

%pre common
CEPH_GROUP_ID=167
CEPH_USER_ID=167
/usr/sbin/groupadd ceph -g $CEPH_GROUP_ID -o -r 2>/dev/null || :
/usr/sbin/useradd ceph -u $CEPH_USER_ID -o -r -g ceph -s /sbin/nologin -c "Ceph daemons" -d %{_localstatedir}/lib/ceph 2>/dev/null || :
exit 0

%post common
%tmpfiles_create %{_tmpfilesdir}/ceph-common.conf

%postun common
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf %{_localstatedir}/log/ceph
    rm -rf %{_sysconfdir}/ceph
fi

%files mds
%{_bindir}/ceph-mds
#%{_mandir}/man8/ceph-mds.8*
%{_unitdir}/ceph-mds@.service
%{_unitdir}/ceph-mds.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mds

%post mds
%systemd_post ceph-mds@\*.service ceph-mds.target
/usr/bin/systemctl start ceph-mds.target >/dev/null 2>&1 || :

%preun mds
%systemd_preun ceph-mds@\*.service ceph-mds.target

%postun mds
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-mds@\*.service ceph-mds.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mds@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mgr
%{_bindir}/ceph-mgr
%{_libdir}/ceph/mgr
%{_unitdir}/ceph-mgr@.service
%{_unitdir}/ceph-mgr.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mgr

%post mgr
%systemd_post ceph-mgr@\*.service ceph-mgr.target
/usr/bin/systemctl start ceph-mgr.target >/dev/null 2>&1 || :

%preun mgr
%systemd_preun ceph-mgr@\*.service ceph-mgr.target

%postun mgr
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-mgr@\*.service ceph-mgr.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mgr@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mon
%{_bindir}/ceph-mon
%{_bindir}/ceph-rest-api
%{python_sitelib}/ceph_rest_api.py*
%{_unitdir}/ceph-mon@.service
%{_unitdir}/ceph-mon.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mon

%post mon
%systemd_post ceph-create-keys@\*.service ceph-mon@\*.service ceph-mon.target
/usr/bin/systemctl start ceph-mon.target >/dev/null 2>&1 || :

%preun mon
%systemd_preun ceph-create-keys@\*.service ceph-mon@\*.service ceph-mon.target

%postun mon
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-create-keys@\*.service ceph-mon@\*.service ceph-mon.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-create-keys@\*.service ceph-mon@\*.service > /dev/null 2>&1 || :
  fi
fi

%files fuse
%defattr(-,root,root,-)
%{_bindir}/ceph-fuse
%{_sbindir}/mount.fuse.ceph
%{_unitdir}/ceph-fuse@.service
%{_unitdir}/ceph-fuse.target

%files -n rbd-fuse
%defattr(-,root,root,-)
%{_bindir}/rbd-fuse

%files -n rbd-mirror
%defattr(-,root,root,-)
%{_bindir}/rbd-mirror
%{_unitdir}/ceph-rbd-mirror@.service
%{_unitdir}/ceph-rbd-mirror.target

%post -n rbd-mirror
%systemd_post ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
/usr/bin/systemctl start ceph-rbd-mirror.target >/dev/null 2>&1 || :

%preun -n rbd-mirror
%systemd_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target

%postun -n rbd-mirror
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-rbd-mirror@\*.service > /dev/null 2>&1 || :
  fi
fi

%files -n rbd-nbd
%defattr(-,root,root,-)
%{_bindir}/rbd-nbd

%files radosgw
%defattr(-,root,root,-)
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%{_bindir}/radosgw-token
%{_bindir}/radosgw-object-expirer
%{_bindir}/radosgw-es

%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%dir %{_localstatedir}/lib/ceph/radosgw
%{_unitdir}/ceph-radosgw@.service
%{_unitdir}/ceph-radosgw.target

%post radosgw
%systemd_post ceph-radosgw@\*.service ceph-radosgw.target
/usr/bin/systemctl start ceph-radosgw.target >/dev/null 2>&1 || :

%preun radosgw
%systemd_preun ceph-radosgw@\*.service ceph-radosgw.target

%postun radosgw
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-radosgw@\*.service ceph-radosgw.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-radosgw@\*.service > /dev/null 2>&1 || :
  fi
fi

%files osd
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-objectstore-tool
%{_bindir}/ceph-osd
%{_sbindir}/ceph-disk
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%dir %{_udevrulesdir}
%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
%{_udevrulesdir}/95-ceph-osd.rules
%{_unitdir}/ceph-osd@.service
%{_unitdir}/ceph-osd.target
%{_unitdir}/ceph-disk@.service
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/osd

%post osd
%systemd_post ceph-disk@\*.service ceph-osd@\*.service ceph-osd.target
/usr/bin/systemctl start ceph-osd.target >/dev/null 2>&1 || :

%preun osd
%systemd_preun ceph-disk@\*.service ceph-osd@\*.service ceph-osd.target

%postun osd
test -n "$FIRST_ARG" || FIRST_ARG=$1
%systemd_postun ceph-disk@\*.service ceph-osd@\*.service ceph-osd.target
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-disk@\*.service ceph-osd@\*.service > /dev/null 2>&1 || :
  fi
fi

%files -n libceph-common
%defattr(-,root,root,-)
%{_libdir}/ceph/libceph-common.so*


%files -n librados2
%defattr(-,root,root,-)
%{_libdir}/librados.so.*
%if %{with lttng}
%{_libdir}/librados_tp.so.*
%endif

%post -n librados2
/sbin/ldconfig

%postun -n librados2
/sbin/ldconfig

%files -n librados-devel
%defattr(-,root,root,-)
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/buffer_fwd.h
%{_includedir}/rados/inline_memory.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/memory.h
%{_libdir}/librados.so
%if %{with lttng}
%{_libdir}/librados_tp.so
%endif
%{_bindir}/librados-config

%files -n python-rados
%defattr(-,root,root,-)
%{python_sitearch}/rados.so
%{python_sitearch}/rados-*.egg-info

%files -n python3-rados
%defattr(-,root,root,-)
%{_libdir}/python3.6/site-packages/rados.cpython*.so
%{_libdir}/python3.6/site-packages/rados-*.egg-info

%files -n libradosstriper1
%defattr(-,root,root,-)
%{_libdir}/libradosstriper.so.*

%post -n libradosstriper1
/sbin/ldconfig

%postun -n libradosstriper1
/sbin/ldconfig

%files -n libradosstriper-devel
%defattr(-,root,root,-)
%dir %{_includedir}/radosstriper
%{_includedir}/radosstriper/libradosstriper.h
%{_includedir}/radosstriper/libradosstriper.hpp
%{_libdir}/libradosstriper.so

%files -n librbd1
%defattr(-,root,root,-)
%{_libdir}/librbd.so.*
%if %{with lttng}
%{_libdir}/librbd_tp.so.*
%endif

%post -n librbd1
/sbin/ldconfig
mkdir -p /usr/lib64/qemu/
ln -sf %{_libdir}/librbd.so.1 /usr/lib64/qemu/librbd.so.1

%postun -n librbd1
/sbin/ldconfig

%files -n librbd-devel
%defattr(-,root,root,-)
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/librbd.so
%if %{with lttng}
%{_libdir}/librbd_tp.so
%endif

%files -n librgw2
%defattr(-,root,root,-)
%{_libdir}/librgw.so.*

%post -n librgw2
/sbin/ldconfig

%postun -n librgw2
/sbin/ldconfig

%files -n librgw-devel
%defattr(-,root,root,-)
%dir %{_includedir}/rados
%{_includedir}/rados/librgw.h
%{_includedir}/rados/rgw_file.h
%{_includedir}/rados/objclass.h
%{_libdir}/librgw.so

%files -n python-rgw
%defattr(-,root,root,-)
%{python_sitearch}/rgw.so
%{python_sitearch}/rgw-*.egg-info

%files -n python3-rgw
%defattr(-,root,root,-)
%{_libdir}/python3.6/site-packages/rgw.cpython*.so
%{_libdir}/python3.6/site-packages/rgw-*.egg-info

%files -n python-rbd
%defattr(-,root,root,-)
%{python_sitearch}/rbd.so
%{python_sitearch}/rbd-*.egg-info

%files -n python3-rbd
%defattr(-,root,root,-)
%{_libdir}/python3.6/site-packages/rbd.cpython*.so
%{_libdir}/python3.6/site-packages/rbd-*.egg-info

%files -n libcephfs2
%defattr(-,root,root,-)
%{_libdir}/libcephfs.so.*

%post -n libcephfs2
/sbin/ldconfig

%postun -n libcephfs2
/sbin/ldconfig

%files -n libcephfs-devel
%defattr(-,root,root,-)
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%{_includedir}/cephfs/ceph_statx.h
%{_libdir}/libcephfs.so

%files -n python-cephfs
%defattr(-,root,root,-)
%{python_sitearch}/cephfs.so
%{python_sitearch}/cephfs-*.egg-info
%{python_sitelib}/ceph_volume_client.py*
%{python_sitelib}/ceph_volume/*
%{python_sitearch}/ceph_volume-*.egg-info

%files -n python3-cephfs
%defattr(-,root,root,-)
%{_libdir}/python3.6/site-packages/cephfs.cpython*.so
%{_libdir}/python3.6/site-packages/cephfs-*.egg-info
%{_libdir}/python3.6/site-packages/ceph_volume_client.py

%files -n python3-ceph-argparse
%defattr(-,root,root,-)
%{_libdir}/python3.6/site-packages/ceph_argparse.py
%{_libdir}/python3.6/site-packages/ceph_daemon.py


%files -n python-ceph-compat
# We need an empty %%files list for python-ceph-compat, to tell rpmbuild to
# actually build this meta package.

%changelog
*   Mon Mar 25 2019 Ankit Jain <ankitja@vmware.com> 12.2.4-3
-   fix CVE-2018-16889
*   Mon Oct 08 2018 Ankit Jain <ankitja@vmware.com> 12.2.4-2
-   fix CVE-2018-10861
*   Thu Apr 19 2018 Xiaolin Li <xiaolinl@vmware.com> 12.2.4-1
-   Updated to version 12.2.4, fix CVE-2018-7262
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 11.2.0-10
-   Requires /bin/grep, /usr/bin/which, or toybox
*   Tue Aug 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 11.2.0-9
-   Add version and release number to python-ceph
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 11.2.0-8
-   Add gdbm-devel to BuildRequires
*   Thu Jun 08 2017 Xiaolin Li <xiaolinl@vmware.com> 11.2.0-7
-   Add python3-setuptools and python3-xml to Buildrequires.
*   Mon May 8 2017 Bo Gan <ganb@vmware.com> 11.2.0-6
-   Fix librados2 dependency
*   Thu Apr 27 2017 Siju Maliakkal <smaliakkal@vmware.com> 11.2.0-5
-   updated python3 version
*   Wed Mar 15 2017 Dheeraj Shetty <Dheerajs@vmware.com> 11.2.0-4
-   corrected version number
*   Mon Mar 13 2017 Dheeraj Shetty <Dheerajs@vmware.com> 11.2.0-3
-   change the python2 path variable
*   Fri Feb 24 2017 Dheeraj Shetty <Dheerajs@vmware.com> 11.2.0-2
-   Turned off switch to build test package
*   Fri Jan 27 2017 Dheeraj Shetty <Dheerajs@vmware.com> 11.2.0-1
-   Initial build. First version based on ceph github repo with modifications for photon
