Summary:	Command Line XML Toolkit
Name:   	xmlstarlet
Version:	1.6.1
Release:	1%{?dist}
License:	MIT
URL:    	http://xmlstar.sourceforge.net/
Group:  	Text Tools
Vendor: 	VMware, Inc.
Distribution:   Photon
Source0:	http://downloads.sourceforge.net/xmlstar/%{name}-%{version}.tar.gz
%define sha1 xmlstarlet=87bb104f546caca71b9540807c5b2738944cb219
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
%setup -q
%patch0 -p1

%build
autoreconf -sif
%configure \
        --with-libxml-prefix=%{_prefix} \
        --with-libxslt-prefix=%{_prefix}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make check

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc %{_mandir}/man1/xmlstarlet.1*
%{_docdir}/xmlstarlet
%{_bindir}/xml


%changelog
* Wed Aug 12 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.1-1
- Initial Release
