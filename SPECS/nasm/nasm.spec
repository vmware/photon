Summary:        Netwide Assembler.
Name:           nasm
Version:        2.15.05
Release:        1%{?dist}
License:        BSD
URL:            http://www.nasm.us
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64
Source0:        http://www.nasm.us/pub/nasm/releasebuilds/%{version}/nasm-%{version}.tar.xz
%define sha1    nasm=d338409a03fc6d1508102881a675a00275fcb879
Source1:        http://www.nasm.us/pub/nasm/releasebuilds/2.15.05/nasm-2.15.05-xdoc.tar.xz
%define sha1    nasm-%{version}-xdoc=3ea5c4fd84c9611a9c0378bebdbd1463413a3191

%description
NASM (Netwide Assembler) is an 80x86 assembler designed for portability and modularity.
It includes a disassembler as well.

%package        doc
Summary:        Detailed manual for the Netwide Assembler

%description    doc
Extensive documentation for the Netwide Assembler (NASM) in HTML and PDF formats.

%package        rdoff
Summary:        Tools for the RDOFF binary format, sometimes used with NASM.

%description    rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM).  These tools
include linker, library manager, loader, and information dump.

%prep
%setup -qn nasm-%{version}
cd ../
tar xf %{SOURCE1} --no-same-owner

%build
./autogen.sh
%configure --enable-sections
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_docdir}
make INSTALLROOT=%{buildroot} install install_rdf

# copy binaries for nasm
cp nasm %{buildroot}/%{_bindir}/
cp ndisasm %{buildroot}/%{_bindir}/
cp nasm.1* %{buildroot}/%{_mandir}/man1/
cp ndisasm.1* %{buildroot}/%{_mandir}/man1/

# copy binaries for nasm-rdoff
cp rdoff/ldrdf %{buildroot}/%{_bindir}/
cp rdoff/rdf2* %{buildroot}/%{_bindir}/
rm %{buildroot}/%{_bindir}/rdf2*.*
cp rdoff/rdfdump %{buildroot}/%{_bindir}/
cp rdoff/rdflib %{buildroot}/%{_bindir}/
cp rdoff/rdx %{buildroot}/%{_bindir}/
cp rdoff/ldrdf.1* %{buildroot}/%{_mandir}/man1/
cp rdoff/rd*.1* %{buildroot}/%{_mandir}/man1/

# copy doc files
mkdir -p %{buildroot}/%{_docdir}/html
cp -r doc/html/*.html %{buildroot}/%{_docdir}/html/
cp doc/*.pdf %{buildroot}/%{_docdir}/
cp doc/*.txt %{buildroot}/%{_docdir}/
cp doc/*.ps %{buildroot}/%{_docdir}/

%check
make %{?_smp_mflags} -k test

%files
%defattr(-,root,root)
%{_bindir}/nasm
%{_bindir}/ndisasm
%{_mandir}/man1/nasm.1*
%{_mandir}/man1/ndisasm.1*

%files doc
%{_docdir}/html/*.html
%{_docdir}/*.pdf
%{_docdir}/*.txt
%{_docdir}/*.ps

%files rdoff
%{_bindir}/ldrdf
%{_bindir}/rdf2bin
%{_bindir}/rdf2com
%{_bindir}/rdf2ihx
%{_bindir}/rdf2ith
%{_bindir}/rdf2srec
%{_bindir}/rdfdump
%{_bindir}/rdflib
%{_bindir}/rdx
%{_mandir}/man1/ldrdf.1*
%{_mandir}/man1/rd*.1*

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.15.05-1
-   Automatic Version Bump
*   Wed Apr 01 2020 Alexey Makhalov <amakhalov@vmware.com> 2.13.03-3
-   Fix compilation issue with gcc-8.4.0
*   Thu Feb 28 2019 Keerthana K <keerthanak@vmware.com> 2.13.03-2
-   Adding BuildArch.
*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.03-1
-   Upgrade version to 2.13.03
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.12.02-1
-   Initial version
