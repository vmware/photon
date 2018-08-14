Summary:	w3m is a text-based web browser
Name:           w3m
Version:        0.5.3
Release:        1%{?dist}
License:        ISC
Group:          Productivity/Networking/Other
Vendor:         VMware, Inc.
Distribution:   Photon
## http://w3m.sourceforge.net
Url:            https://github.com/tats/w3m/archive/v%{version}+git20180125.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}=49df4a9c35f94c211ba2d904f7c72b8aa82e269d
BuildRequires:	gc-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel

%description
w3m is a pager with WWW capability. It IS a pager, but it can be
used as a text-mode WWW browser.

The features of w3m are as follows:

* When reading HTML document, you can follow links and view images
  (using external image viewer).
* It has 'internet message mode', which determines the type of document
  from header. If the Content-Type: field of the document is text/html,
  that document is displayed as HTML document.
* You can change URL description like 'http://hogege.net' in plain text
  into link to that URL.

%prep
%setup -q -n %{name}-%{version}-git20180125

%build
%configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
sed -i 's/require "w3mhelp-funcname.pl/require "\/usr\/share\/w3m\/w3mhelp-funcname.pl/g' %{buildroot}%{_prefix}/libexec/%{name}/cgi-bin/w3mhelp.cgi
sed -i 's/require "w3mhelp-funcdesc.en.pl/require "\/usr\/share\/w3m\/w3mhelp-funcdesc.en.pl/g' %{buildroot}%{_prefix}/libexec/%{name}/cgi-bin/w3mhelp.cgi

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/w3mman
%doc doc/*
%doc ChangeLog
%{_prefix}/libexec
%{_mandir}
%{_datadir}

%changelog
*   Tue Aug 14 2018 Ankit Jain <ankitja@vmware.com> 0.5.3-1
-   Initial Version.
