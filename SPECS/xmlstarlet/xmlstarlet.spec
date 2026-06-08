%global build_if %{photon_subrelease} >= 91
Summary:        Command Line XML Toolkit
Name:           xmlstarlet
Version:        1.6.1
Release:        8%{?dist}
URL:            http://xmlstar.sourceforge.net/
Group:          Text Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/xmlstar/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

#https://sourceforge.net/p/xmlstar/bugs/109/
Patch0:         xmlstarlet-1.6.1-nogit.patch

BuildRequires:  gcc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  linux-api-headers
BuildRequires:  diffutils
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
# libxml2 2.13+ removed ATTRIBUTE_UNUSED from public headers; supply it via
# a forced-include compat header to avoid parenthesis quoting problems with -D.
cat > compat_libxml2.h << 'COMPAT_EOF'
#ifndef ATTRIBUTE_UNUSED
# define ATTRIBUTE_UNUSED __attribute__((__unused__))
#endif
COMPAT_EOF
autoreconf -sif
# libxml2 2.14+ changed xmlStructuredErrorFunc to use const xmlError*; GCC 14
# promotes -Wincompatible-pointer-types to a hard error by default in C code.
# Also suppress deprecated-declarations and pointer-sign for APIs changed in libxml2 2.14+.
export CFLAGS="%{optflags} -Wno-error=incompatible-pointer-types -Wno-error=pointer-sign -Wno-deprecated-declarations -include $(pwd)/compat_libxml2.h"
%configure \
    --with-libxml-prefix=%{_prefix} \
    --with-libxslt-prefix=%{_prefix}

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc %{_mandir}/man1/xmlstarlet.1*
%{_docdir}/xmlstarlet
%{_bindir}/xml

%changelog
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.6.1-8
- Release version bump as part of libxml2/libxslt
* Tue Jul 29 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.6.1-7
- Handle unintended copyrights inclusions
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.6.1-6
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.6.1-5
- Bump version as a part of libxml2 upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.1-4
- Bump version as a part of libxslt upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.6.1-3
- Bump version as a part of libxslt upgrade
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.6.1-2
- Release bump up to use libxml2 2.9.12-1.
* Wed Aug 12 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.1-1
- Initial Release
