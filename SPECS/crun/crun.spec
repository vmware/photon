Name:          crun
Version:       1.4.5
Release:       1%{?dist}
Summary:       OCI runtime in C
License:       GPLv2+
Group:         Development/Other
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/containers/crun
Source0:       https://github.com/containers/crun/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 crun=78715e4a40ad647033a550a71369ee7a6d9325ab0235db858747ab44fbcd29ef1e92e2873ea1ecb2d2d219bac1dba3083a3f3de4145570a5aa742fb188a40790

BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: systemd-devel
BuildRequires: python3
BuildRequires: yajl-devel

Requires:      glibc
Requires:      libcap
Requires:      libseccomp
Requires:      systemd

%description
A fast and low-memory footprint OCI Container Runtime fully written in C

%prep
%autosetup -n %{name}-%{version}

%build
./autogen.sh

%configure \
        --disable-silent-rules \
        --enable-embedded-yajl=yes
%make_build

%install
%make_install
rm -f %{buildroot}%{_prefix}/lib/*.la \
      %{buildroot}%{_prefix}/lib/*.a

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/%{name}
%{_mandir}/*

%changelog
* Wed Jun 08 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.5-1
- crun initial build
