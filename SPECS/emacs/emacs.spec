Summary:        GNU Emacs text editor 
Name:           emacs
Version:        26.1
Release:        1%{?dist}
License:        LGPLv3+
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         ftp://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.gz
%define sha1 emacs=278c4873693173136fb7503ec75cefa32d2ab658

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%prep
%setup -q

%build
%configure --with-jpeg=no --with-png=no --with-gif=no --with-tiff=no --with-gpm=no --with-gnutls=no
make 

%install
cd /usr/src/photon/BUILD/emacs-26.1/
make DESTDIR=%{buildroot} install
echo %{buildroot}
rm -rvf %{buildroot}/usr/lib/debug/
rm -rvf %{buildroot}/usr/bin/ctags
rm -rvf %{buildroot}/usr/share/man/man1/ctags.1.gz

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/*

%changelog
* Thu Jul 5 2018 Ajay Kaher <akaher@vmware.com> 26.1-1
- Initial version

