Name:           mlocate
Version:        0.26
Release:        3%{?dist}
Summary:        An utility for finding files by name.
License:        GPL-2.0
URL:            https://pagure.io/mlocate
Source0:        http://releases.pagure.org/mlocate/%{name}-%{version}.tar.xz
%define sha512  %{name}=b1207047e30a551cba39e70812439b554def567ebe9b8b81fed6f26435bb575beafe4875a21cd72876eadd85da4e7bfc942eb28b17c430b537c351690364837f
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
%autosetup -p1 -n %{name}-%{version}

%build
%configure \
	--enable-nls \
	--disable-rpath
%make_build

%check
make %{?_smp_mflags} check

%install
%make_install DESTDIR=%{buildroot}
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
*   Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.26-3
-   Bump version as a part of gettext upgrade
*   Thu Nov 15 2018 Sujay G <gsujay@vware.com> 0.26-2
-   Added %check section
*   Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 0.26-1
-   Initial mlocate package for Photon.
