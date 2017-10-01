# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

# Got the intial spec from Fedora and modified it
Summary:	An enhanced version of csh, the C shell
Name:		tcsh
Version:	6.19.00
Release:	7%{?dist}
License:	BSD
Group:		System Environment/Shells
Source:		http://www.sfr-fresh.com/unix/misc/%{name}-%{version}.tar.gz
%define sha1 tcsh=cdb1abe319fab5d3caff101c393293e5b3607f0c
Patch0:         tcsh-6.19.00-calloc-gcc-5.patch
URL:		http://www.tcsh.org/
Vendor:		VMware, Inc.
Distribution: 	Photon
Provides:	csh = %{version}
Provides:	/bin/tcsh, /bin/csh
BuildRequires:	ncurses-devel >= 6.0-3
Requires:	ncurses >= 6.0-3
Requires(post): grep
Requires(postun): coreutils, grep

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
make %{?_smp_mflags} -C nls catalogs

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
make check

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
  if [ ! -f /etc/shells ]; then
   echo "%{_bindir}/tcsh" >> /etc/shells
   echo "%{_bindir}/csh"	>> /etc/shells
   echo "/bin/tcsh" >> /etc/shells
   echo "/bin/csh"	>> /etc/shells
  else
   grep -q '^%{_bindir}/tcsh$' /etc/shells || \
   echo "%{_bindir}/tcsh" >> /etc/shells
   grep -q '^%{_bindir}/csh$'  /etc/shells || \
   echo "%{_bindir}/csh"	>> /etc/shells
   grep -q '^/bin/tcsh$' /etc/shells || \
   echo "/bin/tcsh" >> /etc/shells
   grep -q '^/bin/csh$'  /etc/shells || \
   echo "/bin/csh"	>> /etc/shells
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
*   Fri Sep 29 2017 Xiaolin Li <xiaolinl@vmware.com> 6.19.00-7
-   Fix tcsh.lang.
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 6.19.00-6
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue Feb 7 2017 Divya Thaluru <dthaluru@vmware.com> 6.19.00-5
-   Added /bin/tcsh and /bin/csh entries in /etc/shells
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
