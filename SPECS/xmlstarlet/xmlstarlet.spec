Summary:	Command Line XML Toolkit
Name:   	xmlstarlet
Version:	1.6.1
Release:	3%{?dist}
License:	MIT
URL:    	http://xmlstar.sourceforge.net/
Group:  	Text Tools
Vendor: 	VMware, Inc.
Distribution:   Photon
Source0:	http://downloads.sourceforge.net/xmlstar/%{name}-%{version}.tar.gz
%define sha512  xmlstarlet=4228df812caec7059d7a76986c4d9a4262bd861cc53dca05f341ae6c062be05f1c39fc637918ab00f60f40587c6c556e3c9bfaf8a18b149e3c321a92214dbe8b
#https://sourceforge.net/p/xmlstar/bugs/109/
Patch0: 	xmlstarlet-1.6.1-nogit.patch
BuildRequires:  gcc
BuildRequires:  automake autoconf linux-api-headers diffutils
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
Requires:       libxml2
Requires:       libxslt

%description
XMLStarlet is a set of command line utilities which can be used
to transform, query, validate, and edit XML documents and files
using simple set of shell commands in similar way it is done for
plain text files using UNIX grep, sed, awk, diff, patch, join, etc
commands.

%prep
%autosetup -p1

%build
autoreconf -sif
%configure \
        --with-libxml-prefix=%{_prefix} \
        --with-libxslt-prefix=%{_prefix}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

%check
make check %{?_smp_mflags}

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc %{_mandir}/man1/xmlstarlet.1*
%{_docdir}/xmlstarlet
%{_bindir}/xml

%changelog
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.6.1-3
- Bump version as a part of libxslt upgrade
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.6.1-2
- Release bump up to use libxml2 2.9.12-1.
* Wed Aug 12 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.1-1
- Initial Release
