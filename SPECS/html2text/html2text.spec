%define debug_package %{nil}
Summary:	An HTML-to-text converter
Name:		html2text
Version:	1.3.2a
Release:	1%{?dist}
License:	GPL
Group:		Applications/Text
Vendor:         VMware, Inc.
Distribution:   Photon
URL:		http://www.mbayer.de/html2text/
Source:		ftp://ftp.ibiblio.org/pub/linux/apps/www/converters/%{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}.tar.gz=91d46e3218d05b0783bebee96a14f0df0eb9773e

%description
html2text is a command line utility that converts HTML documents into
plain text.
html2text reads HTML documents from standard input or a (local or remote)
URI, and formats them into a stream of plain text characters that is written
to standard output or into an output-file, preserving the original positions
of table fields.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -vdm 755 %{buildroot}
install -vdm 755 %{buildroot}%{_bindir}
install -s -m 755 %{name} %{buildroot}%{_bindir}/
install -vdm 755 %{buildroot}%{_mandir}
install -vdm 755 %{buildroot}%{_mandir}/man1
install -vdm 755 %{buildroot}%{_mandir}/man5
install -m 644 html2text.1.gz %{buildroot}%{_mandir}/man1/
install -m 644 html2textrc.5.gz %{buildroot}%{_mandir}/man5/
install -vdm 755 %{buildroot}%{_datadir}/doc/%{name}
install -p -m 644 CHANGES COPYING CREDITS KNOWN_BUGS README RELEASE_NOTES TODO %{buildroot}%{_datadir}/doc/%{name}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%doc %{_datadir}/doc/%{name}
%doc %{_mandir}

%changelog
*   Tue Aug 14 2018 Ankit Jain <ankitja@vmware.com> 1.3.2a-1
-   Initial Version.
