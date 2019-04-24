Summary:  Bourne-Again SHell
Name:     bash
Version:  4.3.48
Release:  3%{?dist}
License:  GPLv3
URL:      https://www.gnu.org/software/bash/
Group:    System Environment/Base
Vendor:   VMware, Inc.
Distribution: Photon
Source0:  http://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz
%define   sha1 bash=45ac3c5727e7262334f4dfadecdf601b39434e84

#Upstream patches
Patch001: bash43-001
Patch002: bash43-002
Patch003: bash43-003
Patch004: bash43-004
Patch005: bash43-005
Patch006: bash43-006
Patch007: bash43-007
Patch008: bash43-008
Patch009: bash43-009
Patch010: bash43-010
Patch011: bash43-011
Patch012: bash43-012
Patch013: bash43-013
Patch014: bash43-014
Patch015: bash43-015
Patch016: bash43-016
Patch017: bash43-017
Patch018: bash43-018
Patch019: bash43-019
Patch020: bash43-020
Patch021: bash43-021
Patch022: bash43-022
Patch023: bash43-023
Patch024: bash43-024
Patch025: bash43-025
Patch026: bash43-026
Patch027: bash43-027
Patch028: bash43-028
Patch029: bash43-029
Patch030: bash43-030
Patch031: bash43-031
Patch032: bash43-032
Patch033: bash43-033
Patch034: bash43-034
Patch035: bash43-035
Patch036: bash43-036
Patch037: bash43-037
Patch038: bash43-038
Patch039: bash43-039
Patch040: bash43-040
Patch041: bash43-041
Patch042: bash43-042
Patch043: bash43-043
Patch044: bash43-044
Patch045: bash43-045
Patch046: bash43-046
Patch047: bash43-047
Patch048: bash43-048
#https://ftp.gnu.org/gnu/bash/bash-4.4-patches/bash44-006
# with patchlevel removed.
Patch440: bash-CVE-2016-9401.patch

Patch500:   fix-save_bash_input-segfault.patch
Patch501:   bash-4.3.patch
Patch502:   bash-CVE-2019-9924.patch

Provides: /bin/sh
Provides: /bin/bash
Requires(post): ncurses
Requires(post): readline
%description
The package contains the Bourne-Again SHell

%package lang
Summary: Additional language files for bash
Group: System Environment/Base
Requires: %{name} == %{version}-%{release}
%description lang
These are the additional language files of bash.

%prep
%setup -q -n bash-4.3

%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0

%patch440 -p0
%patch500 -p1
%patch501 -p1
%patch502 -p1

%build
%configure --bindir=/bin \
  --without-bash-malloc \
  --with-installed-readline 
make %{?_smp_mflags}
#check if the bash version matches our spec file
BASHVERSION="$(./bashversion -r).$(./bashversion -v).$(./bashversion -p)"
if [ "$BASHVERSION" != "%{version}" ]; then
  echo "Please update the bash version to $BASHVERION" >&2
  exit 1
fi

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
%{_sysconfdir}/bash.bashrc
%{_sysconfdir}/dircolors
%{_sysconfdir}/profile.d/*
%{_sysconfdir}/skel/.bashrc
%{_sysconfdir}/skel/.bash_logout
%{_sysconfdir}/skel/.bash_profile

%doc %{_defaultdocdir}/%{name}
%doc %{_mandir}/*/*

%files lang -f %{name}.lang
#%defattr(-,root,root)

%changelog
*   Wed Apr 24 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.3.48-3
-   Fix CVE-2019-9924
*   Mon Nov 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.48-2
-   Fix CVE-2016-9401.
*   Thu Oct 19 2017 Bo Gan <ganb@vmware.com> 4.3.48-1
-   Upstream patch level 48 applied
-   Fix rpm version to match upstream patch level
-   Address CVE-2016-0634
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
