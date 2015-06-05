Summary:	Docbook-xsl-1.78.1
Name:		docbook-xsl
Version:	1.78.1
Release:	2%{?dist}
License:	Apache License
URL:		http://www.docbook.org
Source0:	http://downloads.sourceforge.net/docbook/%{name}-%{version}.tar.bz2
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	libxml2
BuildRequires:	libxml2
%description
The DocBook XML DTD-4.5 package contains document type definitions for 
verification of XML data files against the DocBook rule set. These are 
useful for structuring books and software documentation to a standard 
allowing you to utilize transformations already written for that standard.
%prep
%setup -q
%build
%install
install -v -m755 -d %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.78.1 &&

cp -v -R VERSION common eclipse epub extensions fo highlighting html \
         htmlhelp images javahelp lib manpages params profiling \
         roundtrip slides template tests tools webhelp website \
         xhtml xhtml-1_1 \
    %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.78.1

pushd %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.78.1
ln -s VERSION VERSION.xsl
popd

install -v -m644 -D README \
                    %{buildroot}%{_docdir}/%{name}-%{version}/README.txt &&
install -v -m644    RELEASE-NOTES* NEWS* \
                    %{buildroot}%{_docdir}/%{name}-%{version}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
if [ ! -d /etc/xml ]; then install -v -m755 -d /etc/xml; fi &&
if [ ! -f /etc/xml/catalog ]; then
    xmlcatalog --noout --create /etc/xml/catalog
fi &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/1.78.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.78.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/1.78.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.78.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.78.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.78.1" \
    /etc/xml/catalog
%postun
rm -rf /etc/xml/catalog

%files
%defattr(-,root,root)
/usr/share/xml/docbook/*
%{_docdir}/*

%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.78.1-2
-   Updated group.
*	Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.78.1-1
-	Initial build. First version
