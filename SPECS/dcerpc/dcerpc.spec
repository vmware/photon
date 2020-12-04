Summary:        DCERPC
Name:           dcerpc
Version:        1.2.0
Release:        2%{?dist}
License:        Novell DCE-RPC - BSD
URL:            https://github.com/vmware/likewise-open/tree/lcifs/dcerpc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        dcerpc-%{version}.tar.gz
%define sha1    dcerpc=63abc1d5d1c421baabc5442b9b9a1a7653ef4271
Patch0:         fix_arm_build.patch
BuildRequires:  krb5-devel
BuildRequires:  curl-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  util-linux-devel
Requires:       curl
Requires:       krb5
Requires:       e2fsprogs

%description
This package provides support for developing DCE RPC applications on the Linux platform.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -fi
export CFLAGS="-Wno-error=unused-but-set-variable -Wno-error=implicit-function-declaration -Wno-error=sizeof-pointer-memaccess -Wno-error=unused-local-typedefs -Wno-error=pointer-sign -Wno-error=address -Wno-unused-but-set-variable -Wno-unused-const-variable -Wno-misleading-indentation -Wno-error=format-overflow -Wno-error=format-truncation -Wno-maybe-uninitialized"
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/dceidl
%{_bindir}/idl
%{_bindir}/uuid
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc.so.1
%{_libdir}/libdcerpc.so.1.0.2
%{_sbindir}/dcerpcd
%{_datadir}/config/dcerpcd.reg

%files devel
%defattr(-,root,root)
%{_includedir}/dce/http.h
%{_includedir}/lwrpcrt/lwrpcrt.h
%{_includedir}/compat/baserpc.h
%{_includedir}/compat/dce2msrpc.h
%{_includedir}/compat/dcerpc.h
%{_includedir}/compat/dcerpc.idl.include
%{_includedir}/compat/rpcfields.h
%{_includedir}/dce/codesets.h
%{_includedir}/dce/codesets.idl
%{_includedir}/dce/codesets_stub.h
%{_includedir}/dce/conv.h
%{_includedir}/dce/conv.idl
%{_includedir}/dce/convc.h
%{_includedir}/dce/convc.idl
%{_includedir}/dce/dce.h
%{_includedir}/dce/dce_error.h
%{_includedir}/dce/dce_utils.h
%{_includedir}/dce/dcethread.h
%{_includedir}/dce/ep.h
%{_includedir}/dce/ep.idl
%{_includedir}/dce/id_base.h
%{_includedir}/dce/id_base.idl
%{_includedir}/dce/idl_es.h
%{_includedir}/dce/idlbase.h
%{_includedir}/dce/idlddefs.h
%{_includedir}/dce/iovector.h
%{_includedir}/dce/iovector.idl
%{_includedir}/dce/lbase.h
%{_includedir}/dce/lbase.idl
%{_includedir}/dce/linux-gnu/dce.h
%{_includedir}/dce/linux-gnu/dce_error.h
%{_includedir}/dce/linux-gnu/dce_utils.h
%{_includedir}/dce/linux-gnu/sec_authn.h
%{_includedir}/dce/lrpc.h
%{_includedir}/dce/marshall.h
%{_includedir}/dce/mgmt.h
%{_includedir}/dce/mgmt.idl
%{_includedir}/dce/nbase.h
%{_includedir}/dce/nbase.idl
%{_includedir}/dce/ncastat.h
%{_includedir}/dce/ncastat.idl
%{_includedir}/dce/ndr_rep.h
%{_includedir}/dce/ndrold.h
%{_includedir}/dce/ndrold.idl
%{_includedir}/dce/ndrtypes.h
%{_includedir}/dce/rpc.h
%{_includedir}/dce/rpc.idl
%{_includedir}/dce/rpcbase.h
%{_includedir}/dce/rpcbase.idl
%{_includedir}/dce/rpcexc.h
%{_includedir}/dce/rpcpvt.h
%{_includedir}/dce/rpcpvt.idl
%{_includedir}/dce/rpcsts.h
%{_includedir}/dce/rpcsts.idl
%{_includedir}/dce/rpctypes.h
%{_includedir}/dce/rpctypes.idl
%{_includedir}/dce/schannel.h
%{_includedir}/dce/sec_authn.h
%{_includedir}/dce/smb.h
%{_includedir}/dce/stubbase.h
%{_includedir}/dce/twr.h
%{_includedir}/dce/twr.idl
%{_includedir}/dce/uuid.h
%{_includedir}/dce/uuid.idl
%{_includedir}/dce/%{_arch}/marshall.h
%{_includedir}/dce/%{_arch}/ndr_rep.h
%{_includedir}/dce/%{_arch}/ndrtypes.h
%{_includedir}/ncklib/comsoc_sys.h
%{_includedir}/ncklib/cs_s_conv.c
%{_includedir}/ncklib/sysconf.h
%{_datadir}/dcerpc/idl.cat
%exclude %{_libdir}/libdcerpc.la
%exclude %{_libdir}/libdcerpc.a

%changelog
*   Fri Dec 04 2020 Tapas Kundu <tkundu@vmware.com> 1.2.0-2
-   Fix arm build issue.
*   Tue Nov 24 2020 Tapas Kundu <tkundu@vmware.com> 1.2.0-1
-   Initial build.  First version
