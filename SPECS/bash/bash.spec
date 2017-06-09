Summary:  Bourne-Again SHell
Name:   bash
Version:  4.3.30
Release:  10%{?dist}
License:  GPLv3
URL:    http://www.gnu.org/software/bash/
Group:    System Environment/Base
Vendor:   VMware, Inc.
Distribution: Photon
Source0:  http://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
%define sha1 bash=33b1bcc5dca1b72f28b2baeca6efa0d422097964
Patch0:   http://www.linuxfromscratch.org/patches/downloads/bash/bash-4.3.30-upstream_fixes-2.patch
Patch1:   fix-save_bash_input-segfault.patch
Patch2:   bash-4.3.patch
Patch3:   bash-CVE-2016-7543.patch
Provides: /bin/sh
Provides: /bin/bash
Requires(post): ncurses
Requires(post): readline
%description
The package contains the Bourne-Again SHell

%package lang
Summary: Additional language files for bash
Group: System Environment/Base
Requires: bash >= 4.3.30
%description lang
These are the additional language files of bash.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
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

cat > %{buildroot}/etc/bash.bashrc << "EOF"
# Begin /etc/bash.bashrc
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

if test -n "$SSH_CONNECTION" -a -z "$PROFILEREAD"; then
     . /etc/profile > /dev/null 2>&1
fi
# End /etc/bash.bashrc
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

if [ -f "/etc/bash.bashrc" ] ; then
  source /etc/bash.bashrc
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
if [ $1 -eq 1 ] ; then
    if [ ! -f "/root/.bash_logout" ] ; then
        cp /etc/skel/.bash_logout /root/.bash_logout
    fi
    if [ ! -f /etc/shells ]; then
        echo "/bin/sh" >> /etc/shells
        echo "/bin/bash" >> /etc/shells
        echo "%{_bindir}/sh" >> /etc/shells
        echo "%{_bindir}/bash" >> /etc/shells
    else
        grep -q '^/bin/sh$' /etc/shells || \
        echo "/bin/sh" >> /etc/shells
        grep -q '^/bin/bash$' /etc/shells || \
        echo "/bin/bash" >> /etc/shells
        grep -q '^%{_bindir}/sh$' /etc/shells || \
        echo "%{_bindir}/sh" >> /etc/shells
        grep -q '^%{_bindir}/bash$' /etc/shells || \
        echo "%{_bindir}/bash" >> /etc/shells
    fi
fi
if [ $1 -eq 2 ] ; then
    if [ ! -f /etc/shells ]; then
        echo "/bin/sh" >> /etc/shells
        echo "/bin/bash" >> /etc/shells
        echo "%{_bindir}/sh" >> /etc/shells
        echo "%{_bindir}/bash" >> /etc/shells
    else
        grep -q '^/bin/sh$' /etc/shells || \
        echo "/bin/sh" >> /etc/shells
        grep -q '^/bin/bash$' /etc/shells || \
        echo "/bin/bash" >> /etc/shells
        grep -q '^%{_bindir}/sh$' /etc/shells || \
        echo "%{_bindir}/sh" >> /etc/shells
        grep -q '^%{_bindir}/bash$' /etc/shells || \
        echo "%{_bindir}/bash" >> /etc/shells
    fi
fi

%postun
if [ $1 -eq 0 ] ; then
    if [ -f "/root/.bash_logout" ] ; then
        rm -f /root/.bash_logout
    fi
    if [ ! -x /bin/sh ]; then
        grep -v '^/bin/sh$'  /etc/shells | \
        grep -v '^/bin/sh$' > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
    fi
    if [ ! -x /bin/bash ]; then
        grep -v '^/bin/bash$'  /etc/shells | \
        grep -v '^/bin/bash$' > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
    fi
    if [ ! -x %{_bindir}/sh ]; then
        grep -v '^%{_bindir}/sh$'  /etc/shells | \
        grep -v '^%{_bindir}/sh$' > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
    fi
    if [ ! -x %{_bindir}/bash ]; then
        grep -v '^%{_bindir}/bash$'  /etc/shells | \
        grep -v '^%{_bindir}/bash$' > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
    fi
fi

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
*   Fri Jun 9 2017 Bo Gan <ganb@vmware.com> 4.3.30-10
-   Add post dependency
*   Fri Jun 2 2017 Divya Thaluru <dthaluru@vmware.com>  4.3.30-9
-   Added /usr/bin/sh and /bin/sh entries in /etc/shells
*   Tue Apr 04 2017 Anish Swaminathan <anishs@vmware.com> 4.3.30-8
-   Apply patch for CVE-2016-7543
*   Tue Feb 7 2017 Divya Thaluru <dthaluru@vmware.com>  4.3.30-7
-   Added /usr/bin/bash and /bin/bash entries in /etc/shells
*   Thu Feb 2 2017 Divya Thaluru <dthaluru@vmware.com>  4.3.30-6
-   Modified bash entry in /etc/shells
*   Tue Jan 10 2017 Divya Thaluru <dthaluru@vmware.com>  4.3.30-5
-   Added bash entry to /etc/shells
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.3.30-4
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  4.3.30-3
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Mar 10 2016 Divya Thaluru <dthaluru@vmware.com> 4.3.30-2
-   Adding compile options to load bash.bashrc file and
    loading source file during non-inetractive non-login shell
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.3.30-1
-   Updated to version 4.3.30
*   Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 4.3-4
-   Adding post unstall section.
*   Wed Jul 22 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-3
-   Fix segfault in save_bash_input.
*   Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 4.3-2
-   /etc/profile.d permission fix. Pack /etc files into rpm
*   Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 4.3-1
-   Initial version

