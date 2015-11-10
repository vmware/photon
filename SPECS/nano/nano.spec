Summary:	Text editor
Name:		nano
Version:	2.2.6
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.nano-editor.org/
Group:		Applications/Editors
Source0:	http://www.nano-editor.org/dist/v2.2/%{name}-%{version}.tar.gz
%define sha1 nano=f2a628394f8dda1b9f28c7e7b89ccb9a6dbd302a
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Nano package contains a small, simple text editor
%prep
%setup -q -n %{name}-%{version}
%build
./configure --prefix=%{_prefix}      \
            --sysconfdir=%{_sysconfdir} \
            --enable-utf8     \
            --infodir=%{_infodir}/%{name}-%{version} \
            --docdir=%{_docdir}/%{name}-%{version}
make
%install
make DESTDIR=%{buildroot} install
install -v -m644 %{_builddir}/%{name}-%{version}/doc/nanorc.sample %{_sysconfdir}
install -v -m644 %{_builddir}/%{name}-%{version}/doc/texinfo/nano.html %{_docdir}/%{name}-%{version}.html
%find_lang %{name}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*
%{_mandir}/fr/man*/*
%{_infodir}/%{name}-%{version}/*
%{_datadir}/nano/*
%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.2.6-2
-	Handled locale files with macro find_lang
*	Tue Dec 30 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.6-1
-	Initial build.	First version
