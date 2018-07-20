Name:           mlocate
Version:        0.26
Release:        1%{?dist}
Summary:        An utility for finding files by name.
License:        GPL-2.0
URL:            https://pagure.io/mlocate
Source0:        http://releases.pagure.org/mlocate/%{name}-%{version}.tar.xz
%define sha1    %{name}=c6e6d81b25359c51c545f4b8ba0f3b469227fcbc
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/File
BuildRequires:  sed
BuildRequires:  grep
BuildRequires:  xz
BuildRequires:  gettext

%description
mlocate is a locate/updatedb implementation.  The 'm' stands for "merging":
updatedb reuses the existing database to avoid rereading most of the file
system, which makes updatedb faster and does not trash the system caches as
much.

%prep
%setup -q -n %{name}-%{version}

%build
%configure \
	--localstatedir=%{_localstatedir}/lib \
	--enable-nls \
	--disable-rpath
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mv %{buildroot}/%{_bindir}/locate %{buildroot}/%{_bindir}/%{name}
mv %{buildroot}/%{_bindir}/updatedb %{buildroot}/%{_bindir}/updatedb.%{name}
mv %{buildroot}/%{_mandir}/man1/locate.1 %{buildroot}/%{_mandir}/man1/%{name}.1

%files
%defattr(-,root,root,-)
%{_bindir}*
%{_mandir}/*
%{_datarootdir}/locale/*
%{_localstatedir}/*

%changelog
*   Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 0.26-1
-   Initial mlocate package for Photon.
