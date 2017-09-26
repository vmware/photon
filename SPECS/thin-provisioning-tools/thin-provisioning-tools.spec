Summary: 	Thin provisioning tools
Name:		thin-provisioning-tools
Version:	0.6.1
Release:	3%{?dist}
License:	GPLv3+
Group:		System Environment/Base
URL:		https://github.com/jthornber/thin-provisioning-tools
Source0:	https://github.com/jthornber/thin-provisioning-tools/releases/thin-provisioning-tools-%{version}.tar.gz
%define sha1 thin-provisioning-tools=387096be52b2f846b8b83f3d8da8e2cc6775465f
BuildRequires:	expat , libaio-devel, boost-devel
Requires:	expat, libaio
Vendor:		VMware, Inc.
Distribution:	Photon

%description
thin-provisioning-tools contains check,dump,restore,repair,rmap
and metadata_size tools to manage device-mapper thin provisioning
target metadata devices; cache check,dump,metadata_size,restore
and repair tools to manage device-mapper cache metadata devices
are included and era check, dump, restore and invalidate to manage
snapshot eras

%prep
#%setup -q -n thin-provisioning-tools-thin-provisioning-tools-%{version}
%setup -q

%build
autoconf
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} MANDIR=%{_mandir} install

%clean

%files
%doc COPYING README.md
%{_mandir}/man8/cache_check.8.gz
%{_mandir}/man8/cache_dump.8.gz
%{_mandir}/man8/cache_restore.8.gz
%{_mandir}/man8/cache_repair.8.gz
%{_mandir}/man8/era_check.8.gz
%{_mandir}/man8/era_dump.8.gz
%{_mandir}/man8/era_invalidate.8.gz
%{_mandir}/man8/thin_check.8.gz
%{_mandir}/man8/thin_dump.8.gz
%{_mandir}/man8/thin_metadata_size.8.gz
%{_mandir}/man8/thin_restore.8.gz
%{_mandir}/man8/thin_repair.8.gz
%{_mandir}/man8/thin_rmap.8.gz
%{_mandir}/man8/thin_delta.8.gz
%{_mandir}/man8/thin_ls.8.gz
%{_mandir}/man8/thin_trim.8.gz
%{_sbindir}/pdata_tools
%{_sbindir}/cache_check
%{_sbindir}/cache_dump
%{_sbindir}/cache_metadata_size
%{_sbindir}/cache_restore
%{_sbindir}/cache_repair
%{_sbindir}/era_check
%{_sbindir}/era_dump
%{_sbindir}/era_restore
%{_sbindir}/era_invalidate
%{_sbindir}/thin_check
%{_sbindir}/thin_dump
%{_sbindir}/thin_metadata_size
%{_sbindir}/thin_restore
%{_sbindir}/thin_repair
%{_sbindir}/thin_rmap
%{_sbindir}/thin_delta
%{_sbindir}/thin_ls
%{_sbindir}/thin_trim

%changelog
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 0.6.1-3
-   Release bump for expat version update
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.1-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 0.6.1-1
- Updating version
* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.4.1-1
- Initial version

