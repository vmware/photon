Summary:        Netwide Assembler.
Name:           nasm
Version:        2.16.01
Release:        1%{?dist}
License:        BSD
URL:            http://www.nasm.us
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      x86_64

Source0: http://www.nasm.us/pub/nasm/releasebuilds/%{version}/nasm-%{version}.tar.xz
%define sha512  %{name}=51fccb5639ce019d9c423c0f279750ffbd74c64cd41dd3b185d1aa1a1aaed79c5d3cd8d4bebbc13ee249a375ed27457ea2abde1a4dbb24d354598fffd1254833
Source1: http://www.nasm.us/pub/nasm/releasebuilds/%{version}/nasm-%{version}-xdoc.tar.xz
%define sha512  %{name}-%{version}-xdoc=ec260c0a537b0172e6f2ac17118c744db8743886388a112e99bab1b8c8fee91547dade69dcfe9a15289b2b1a428e8c009048a468f7982b03dd4506abcafc0787

%description
NASM (Netwide Assembler) is an 80x86 assembler designed for portability and modularity.
It includes a disassembler as well.

%package        doc
Summary:        Detailed manual for the Netwide Assembler

%description    doc
Extensive documentation for the Netwide Assembler (NASM) in HTML and PDF formats.

%prep
%autosetup -n %{name}-%{version}
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
make INSTALLROOT=%{buildroot} install %{?_smp_mflags}

# copy binaries for nasm
cp nasm %{buildroot}/%{_bindir}/
cp ndisasm %{buildroot}/%{_bindir}/
cp nasm.1* %{buildroot}/%{_mandir}/man1/
cp ndisasm.1* %{buildroot}/%{_mandir}/man1/

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

%changelog
* Mon Apr 17 2023 Nitesh Kumar <kunitesh@vmware.com> 2.16.01-1
- Upgrade to v2.16.01 to fix CVE-2021-45257
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.15.05-1
- Automatic Version Bump
* Wed Apr 01 2020 Alexey Makhalov <amakhalov@vmware.com> 2.13.03-3
- Fix compilation issue with gcc-8.4.0
* Thu Feb 28 2019 Keerthana K <keerthanak@vmware.com> 2.13.03-2
- Adding BuildArch.
* Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.13.03-1
- Upgrade version to 2.13.03
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.12.02-1
- Initial version
