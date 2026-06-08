%global build_if %{photon_subrelease} >= 91
Summary:        Docbook-xsl-1.79.1
Name:           docbook-xsl
Version:        1.79.1
Release:        13%{?dist}
URL:            http://www.docbook.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://downloads.sourceforge.net/docbook/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

Requires:       libxml2

BuildRequires:  libxml2
BuildRequires:  python3

BuildArch:      noarch

%description
The DocBook XML DTD-4.5 package contains document type definitions for
verification of XML data files against the DocBook rule set. These are
useful for structuring books and software documentation to a standard
allowing you to utilize transformations already written for that standard.

%prep
%autosetup -p1

%build
# Remove Windows executables from jython.jar (zip is deprecated; use python3 zipfile)
python3 - << 'PYEOF'
import zipfile, os
jar = "tools/lib/jython.jar"
tmp = jar + ".tmp"
remove = {"Lib/distutils/command/wininst-6.exe", "Lib/distutils/command/wininst-7.1.exe"}
with zipfile.ZipFile(jar, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for entry in zin.infolist():
        if entry.filename not in remove:
            zout.writestr(entry, zin.read(entry.filename))
os.replace(tmp, jar)
PYEOF

%install
install -v -m755 -d %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1 &&

cp -v -R VERSION common eclipse epub extensions fo highlighting html \
         htmlhelp images javahelp lib manpages params profiling \
         roundtrip slides template tests tools webhelp website \
         xhtml xhtml-1_1 \
    %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1

pushd %{buildroot}/usr/share/xml/docbook/xsl-stylesheets-1.79.1
rm extensions/saxon65.jar \
   tools/lib/saxon.jar \
   tools/lib/saxon9-ant.jar \
   tools/lib/saxon9he.jar
ln -s VERSION VERSION.xsl
popd

install -v -m644 -D README \
                    %{buildroot}%{_docdir}/%{name}-%{version}/README.txt &&
install -v -m644    RELEASE-NOTES* NEWS* \
                    %{buildroot}%{_docdir}/%{name}-%{version}

#There is no source code for make check
#%%check
#chmod 777 tests -R
#make %{?_smp_mflags} check

%post
if [ ! -d /etc/xml ]; then install -v -m755 -d /etc/xml; fi &&
if [ ! -f /etc/xml/catalog ]; then
    xmlcatalog --noout --create /etc/xml/catalog
fi &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/1.79.1" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteSystem" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog &&

xmlcatalog --noout --add "rewriteURI" \
           "http://docbook.sourceforge.net/release/xsl/current" \
           "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
    /etc/xml/catalog

%postun
if [ $1 -eq 0 ] ; then
    if [ -f /etc/xml/catalog ]; then
        xmlcatalog --noout --del \
        "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" /etc/xml/catalog
    fi
fi

%files
%defattr(-,root,root)
/usr/share/xml/docbook/*
%{_docdir}/*

%changelog
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.79.1-13
- Release version bump as part of libxml2/libxslt
* Tue Jun 02 2026 Ajay Kaher <ajay.kaher@broadcom.com> 1.79.1-12
- Replace deprecated zip with python3 zipfile; add BuildRequires python3
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.79.1-11
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.79.1-10
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.79.1-9
- Bump version as a part of libxml2 upgrade
* Mon Nov 08 2021 Nitesh Kumar <kunitesh@vmware.com> 1.79.1-8
- Release bump up to use libxml2 2.9.12-1.
* Fri Jan 18 2019 Tapas Kundu <tkundu@vmware.com> 1.79.1-7
- Removed saxon jar files while installing
* Tue Dec 04 2018 Ashwin H<ashwinh@vmware.com> 1.79.1-6
- Remove windows installers
* Fri Aug 18 2017 Rongrong Qiu <rqiu@vmware.com> 1.79.1-5
- Update make check for bug 1635477
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.79.1-4
- Fix arch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.79.1-3
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.79.1-2
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 1.79.1-1
- Updated version.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.78.1-2
- Updated group.
* Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.78.1-1
- Initial build. First version
