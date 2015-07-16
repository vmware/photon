# Got the intial spec from Fedora and modified it
Summary:	An enhanced version of csh, the C shell
Name:		tcsh
Version:	6.18.01
Release:	1%{?dist}
License:	BSD
Group:		System Environment/Shells
Source:		http://www.sfr-fresh.com/unix/misc/%{name}-%{version}.tar.gz
%define sha1 tcsh=eee2035645737197ff8059c84933a75d23cd76f9
URL:		http://www.tcsh.org/
Vendor:		VMware, Inc.
Distribution: 	Photon
Provides:	csh = %{version}
Provides:	/bin/tcsh, /bin/csh
BuildRequires:	ncurses-devel
Requires:	ncurses
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
	if test -f tcsh.$language.cat ; then
		mkdir -p $dest
		install -p -m 644 tcsh.$language.cat $dest/tcsh
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
if [ ! -f /etc/shells ]; then
 echo "%{_bindir}/tcsh" >> /etc/shells
 echo "%{_bindir}/csh"	>> /etc/shells
else
 grep -q '^%{_bindir}/tcsh$' /etc/shells || \
 echo "%{_bindir}/tcsh" >> /etc/shells
 grep -q '^%{_bindir}/csh$'  /etc/shells || \
 echo "%{_bindir}/csh"	>> /etc/shells
fi

%postun
if [ ! -x %{_bindir}/tcsh ]; then
 grep -v '^%{_bindir}/tcsh$'  /etc/shells | \
 grep -v '^%{_bindir}/csh$' > /etc/shells.rpm && \
 mv /etc/shells.rpm /etc/shells
fi

%files -f tcsh.lang
%defattr(-,root,root,-)
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*

%changelog
*	Wed Apr 1 2015 Divya Thaluru <dthaluru@vmware.com> 6.18.01-1
-	Initial build. First version
