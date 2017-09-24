# Got the intial spec from Fedora and modified it
Summary:        An enhanced version of csh, the C shell
Name:           tcsh
Version:        6.20.00
Release:        4%{?dist}
License:        BSD
Group:          System Environment/Shells
Source:         http://www.sfr-fresh.com/unix/misc/%{name}-%{version}.tar.xz
%define sha1    tcsh=a52deb0181e32583dbe666474c9c2e784357feba
# patch origin http://pkgs.fedoraproject.org/cgit/rpms/tcsh.git/
Patch0:         tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch
URL:            http://www.tcsh.org/
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       csh = %{version}
Provides:       /bin/tcsh, /bin/csh
BuildRequires:  ncurses-devel
Requires:       ncurses
Requires(post): /bin/grep
Requires(postun): (coreutils or toybox) /bin/grep

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%setup -q
%patch0 -p1

%build
sed -i -e 's|\$\*|#&|' -e 's|fR/g|&m|' tcsh.man2html &&

%configure --prefix=%{_prefix}
make %{?_smp_mflags} all

%install
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}%{_bindir}
install -p -m 755 tcsh %{buildroot}%{_bindir}/tcsh
install -p -m 644 tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1
ln -sf tcsh %{buildroot}%{_bindir}/csh
ln -sf tcsh.1 %{buildroot}%{_mandir}/man1/csh.1

while read lang language ; do
  dest=%{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  if test -f nls/$language.cat ; then
    mkdir -p $dest
    install -p -m 644 nls/$language.cat $dest/tcsh
    echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
  fi
done > tcsh.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

%check
# tcsh expect nonroot user to run a tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
  if [ ! -f /etc/shells ]; then
   echo "%{_bindir}/tcsh" >> /etc/shells
   echo "%{_bindir}/csh"  >> /etc/shells
   echo "/bin/tcsh" >> /etc/shells
   echo "/bin/csh"  >> /etc/shells
  else
   grep -q '^%{_bindir}/tcsh$' /etc/shells || \
   echo "%{_bindir}/tcsh" >> /etc/shells
   grep -q '^%{_bindir}/csh$'  /etc/shells || \
   echo "%{_bindir}/csh"  >> /etc/shells
   grep -q '^/bin/tcsh$' /etc/shells || \
   echo "/bin/tcsh" >> /etc/shells
   grep -q '^/bin/csh$'  /etc/shells || \
   echo "/bin/csh"  >> /etc/shells
  fi
fi

%postun
if [ $1 -eq 0 ] ; then
  if [ ! -x %{_bindir}/tcsh ]; then
   grep -v '^%{_bindir}/tcsh$'  /etc/shells | \
   grep -v '^%{_bindir}/csh$' > /etc/shells.rpm && \
   mv /etc/shells.rpm /etc/shells
  fi
  if [ ! -x /bin/tcsh ]; then
   grep -v '^/bin/tcsh$'  /etc/shells | \
   grep -v '^/bin/csh$' > /etc/shells.rpm && \
   mv /etc/shells.rpm /etc/shells
  fi
fi

%files -f tcsh.lang
%defattr(-,root,root,-)
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*

%changelog
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 6.20.00-4
-   Requires coreutils or toybox and /bin/grep
*   Tue Jun 6 2017 Alexey Makhalov <amakhalov@vmware.com> 6.20.00-3
-   Fix make check issues.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.20.00-2
-   Ensure non empty debuginfo
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.20.00-1
-   Updated to version 6.20.00
*   Tue Feb 07 2017 Divya Thaluru <dthaluru@vmware.com> 6.19.00-6
-   Added /bin/csh and /bin/tsch entries in /etc/shells
*   Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 6.19.00-5
-   tcsh.glibc-2.24.patch
*   Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> 6.19.00-4
-   Fix calloc for gcc 5 optimization
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.19.00-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.19.00-2
-   Fix for upgrade issues
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 6.19.00-1
-   Upgrade version
*   Wed Apr 1 2015 Divya Thaluru <dthaluru@vmware.com> 6.18.01-1
-   Initial build. First version
