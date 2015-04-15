Summary:	Unzip-6.0
Name:		unzip
Version:	6.0
Release:	1
License:	BSD
URL:		http://www.gnu.org/software/%{name}
Source0:	http://downloads.sourceforge.net/infozip/unzip60.tar.gz
Group:		SystemUtilities
Vendor:		VMware, Inc.
Distribution: Photon
%description
The UnZip package contains ZIP extraction utilities. These are useful 
for extracting files from ZIP archives. ZIP archives are created 
with PKZIP or Info-ZIP utilities, primarily in a DOS environment.
%prep
%setup -qn unzip60
%build
case `uname -m` in
  i?86)
    sed -i -e 's/DASM_CRC"/DASM_CRC -DNO_LCHMOD"/' unix/Makefile
    make -f unix/Makefile linux %{?_smp_mflags}
    ;;
  *)
    sed -i -e 's/CFLAGS="-O -Wall/& -DNO_LCHMOD/' unix/Makefile
    make -f unix/Makefile linux_noasm %{?_smp_mflags}
    ;;
esac
%install
install -v -m755 -d %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} prefix=%{_prefix} install
cp %{_builddir}/unzip60/funzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzip %{buildroot}%{_bindir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%changelog
*	Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 6.0-1
-	Initial build. First version
