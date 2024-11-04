Summary:    Program for compiling packages
Name:       make
Version:    4.3
Release:    3%{?dist}
URL:        http://www.gnu.org/software/make
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.gz
%define sha512 %{name}=9a1185cc468368f4ec06478b1cfa343bf90b5cd7c92c0536567db0315b0ee909af53ecce3d44cfd93dd137dbca1ed13af5713e8663590c4fdd21ea635d78496b

Source1: license.txt
%include %{SOURCE1}

%description
The Make package contains a program for compiling packages.

%prep
%autosetup -p1

%build
#work around an error caused by glibc-2.27
# glob.c is at lib/glob.c in make-4.3
sed -i '211,217 d; 219,229 d' lib/glob.c

%configure \
    --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%find_lang %{name}

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gnumake.h
%{_mandir}/*/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.3-3
- Release bump for SRP compliance
* Tue Jan 19 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.3-2
- Fix make check
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3-1
- Automatic Version Bump
* Tue Oct 22 2019 Prashant S Chauhan <psinghchauha@vmware.com> 4.2.1-3
- Fix make check added a patch
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-2
- Fix compilation issue against glibc-2.27
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.2.1-1
- Update package version
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 4.1-4
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1-3
- GA - Bump release of all rpms
* Tue May 10 2016 Kumar Kaushik <kaushikk@vmware.com>  4.1-2
- Fix for segfaults in chroot env.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  4.1-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.0-1
- Initial build. First version
