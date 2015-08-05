Summary:	Bourne-Again SHell
Name:		bash
Version:	4.3
Release:	4%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/bash/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
%define sha1 bash=45ac3c5727e7262334f4dfadecdf601b39434e84
Patch0:		http://www.linuxfromscratch.org/patches/downloads/bash/bash-4.3-upstream_fixes-7.patch
Patch1:		fix-save_bash_input-segfault.patch
Provides:	/bin/sh
Provides:	/bin/bash
%description
The package contains the Bourne-Again SHell

%package lang
Summary: Additional language files for bash
Group: System Environment/Base
Requires: bash >= 4.3
%description lang
These are the additional language files of bash.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--htmldir=%{_defaultdocdir}/%{name}-%{version} \
	--without-bash-malloc \
	--with-installed-readline 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
ln -s bash %{buildroot}/bin/sh
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/etc/profile.d
install -vdm 755 %{buildroot}/etc/skel

# Create dircolors
cat > %{buildroot}/etc/profile.d/dircolors.sh << "EOF"
# Setup for /bin/ls and /bin/grep to support color, the alias is in /etc/bashrc.
if [ -f "/etc/dircolors" ] ; then
        eval $(dircolors -b /etc/dircolors)

        if [ -f "$HOME/.dircolors" ] ; then
                eval $(dircolors -b $HOME/.dircolors)
        fi
fi
alias ls='ls --color=auto'
alias grep='grep --color=auto'
EOF

cat > %{buildroot}/etc/profile.d/extrapaths.sh << "EOF"
if [ -d /usr/local/lib/pkgconfig ] ; then
        pathappend /usr/local/lib/pkgconfig PKG_CONFIG_PATH
fi
if [ -d /usr/local/bin ]; then
        pathprepend /usr/local/bin
fi
if [ -d /usr/local/sbin -a $EUID -eq 0 ]; then
        pathprepend /usr/local/sbin
fi
EOF

cat > %{buildroot}/etc/profile.d/readline.sh << "EOF"
# Setup the INPUTRC environment variable.
if [ -z "$INPUTRC" -a ! -f "$HOME/.inputrc" ] ; then
        INPUTRC=/etc/inputrc
fi
export INPUTRC
EOF

cat > %{buildroot}/etc/profile.d/umask.sh << "EOF"
# By default, the umask should be set.
if [ "$(id -gn)" = "$(id -un)" -a $EUID -gt 99 ] ; then
  umask 002
else
  umask 022
fi
EOF

cat > %{buildroot}/etc/profile.d/i18n.sh << "EOF"
# Begin /etc/profile.d/i18n.sh

unset LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES \
      LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT LC_IDENTIFICATION

if [ -n "$XDG_CONFIG_HOME" ] && [ -r "$XDG_CONFIG_HOME/locale.conf" ]; then
  . "$XDG_CONFIG_HOME/locale.conf"
elif [ -r /etc/locale.conf ]; then
  . /etc/locale.conf
fi

export LANG="${LANG:-C}"
[ -n "$LC_CTYPE" ]          && export LC_CTYPE
[ -n "$LC_NUMERIC" ]        && export LC_NUMERIC
[ -n "$LC_TIME" ]           && export LC_TIME
[ -n "$LC_COLLATE" ]        && export LC_COLLATE
[ -n "$LC_MONETARY" ]       && export LC_MONETARY
[ -n "$LC_MESSAGES" ]       && export LC_MESSAGES
[ -n "$LC_PAPER" ]          && export LC_PAPER
[ -n "$LC_NAME" ]           && export LC_NAME
[ -n "$LC_ADDRESS" ]        && export LC_ADDRESS
[ -n "$LC_TELEPHONE" ]      && export LC_TELEPHONE
[ -n "$LC_MEASUREMENT" ]    && export LC_MEASUREMENT
[ -n "$LC_IDENTIFICATION" ] && export LC_IDENTIFICATION

# End /etc/profile.d/i18n.sh
EOF

cat > %{buildroot}/etc/bashrc << "EOF"
# Begin /etc/bashrc
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>

# System wide aliases and functions.

# System wide environment variables and startup programs should go into
# /etc/profile.  Personal environment variables and startup programs
# should go into ~/.bash_profile.  Personal aliases and functions should
# go into ~/.bashrc

# Provides colored /bin/ls and /bin/grep commands.  Used in conjunction
# with code in /etc/profile.

alias ls='ls --color=auto'
alias grep='grep --color=auto'

# Provides prompt for non-login shells, specifically shells started
# in the X environment. [Review the LFS archive thread titled
# PS1 Environment Variable for a great case study behind this script
# addendum.]

NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
  PS1="$RED\u [ $NORMAL\w$RED ]# $NORMAL"
else
  PS1="$GREEN\u [ $NORMAL\w$GREEN ]\$ $NORMAL"
fi

unset RED GREEN NORMAL

# End /etc/bashrc
EOF


cat > %{buildroot}/etc/skel/.bash_profile << "EOF"
# Begin ~/.bash_profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>

# Personal environment variables and startup programs.

# Personal aliases and functions should go in ~/.bashrc.  System wide
# environment variables and startup programs are in /etc/profile.
# System wide aliases and functions are in /etc/bashrc.

if [ -f "$HOME/.bashrc" ] ; then
  source $HOME/.bashrc
fi

if [ -d "$HOME/bin" ] ; then
  pathprepend $HOME/bin
fi

# Having . in the PATH is dangerous
#if [ $EUID -gt 99 ]; then
#  pathappend .
#fi

# End ~/.bash_profile
EOF

cat > %{buildroot}/etc/skel/.bashrc << "EOF"
# Begin ~/.bashrc
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>

# Personal aliases and functions.

# Personal environment variables and startup programs should go in
# ~/.bash_profile.  System wide environment variables and startup
# programs are in /etc/profile.  System wide aliases and functions are
# in /etc/bashrc.

if [ -f "/etc/bashrc" ] ; then
  source /etc/bashrc
fi

# End ~/.bashrc
EOF

cat > %{buildroot}/etc/skel/.bash_logout << "EOF"
# Begin ~/.bash_logout
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>

# Personal items to perform on logout.

# End ~/.bash_logout
EOF

dircolors -p > %{buildroot}/etc/dircolors

%find_lang %{name}
rm -rf %{buildroot}/%{_infodir}

%post
test -e /root/.bash_profile || cp /etc/skel/.bash_profile /root
test -e /root/.bashrc || cp /etc/skel/.bashrc /root
test -e /root/.bash_logout || cp /etc/skel/.bash_logout /root

%postun
rm -f /root/.bashrc
rm -f /root/.bash_profile
rm -f /root/.bash_logout

%files
%defattr(-,root,root)
/bin/*
%{_sysconfdir}
%{_defaultdocdir}/%{name}-%{version}/*
%{_defaultdocdir}/%{name}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*       Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 4.3-4
-       Adding post unstall section.
*	Wed Jul 22 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-3
-	Fix segfault in save_bash_input.
*	Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-2
-	/etc/profile.d permission fix. Pack /etc files into rpm
*	Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 4.3-1
-	Initial version

