Summary:	Text editor
Name:		nano
Version:	2.5.2
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.nano-editor.org/
Group:		Applications/Editors
Source0:	http://www.nano-editor.org/dist/v2.2/%{name}-%{version}.tar.gz
%define sha1 nano=ee21ed3f3771f6959bf430ab9e80de56026798b8
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	ncurses-devel >= 6.0-3
Requires:	ncurses >= 6.0-3
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
%{_datadir}/doc/nano-2.5.2/*

%changelog
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 2.5.2-3
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.2-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.2-1
-   Updating to new version.
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.2.6-2
-   Handled locale files with macro find_lang
*   Tue Dec 30 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.6-1
-   Initial build.	First version
