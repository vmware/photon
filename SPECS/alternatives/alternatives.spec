%global build_if %{photon_subrelease} >= 91
%define src_name chkconfig

Summary:    Maintain symbolic links determining default commands
Name:       alternatives
Version:    1.32
Release:    4%{?dist}
Group:      System Environment/Base
URL:        https://git.fedorahosted.org/git/chkconfig
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://github.com/fedora-sysv/chkconfig/archive/refs/tags/%{src_name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-makefile-only-install-alternatives.patch

Requires: libselinux
Requires: libsepol
Requires: newt
Requires: popt
Requires: slang
Requires: systemd

BuildRequires: systemd-devel
BuildRequires: newt-devel
BuildRequires: gettext
BuildRequires: popt-devel
BuildRequires: libselinux-devel

Conflicts: initscripts <= 5.30-1
Obsoletes: chkconfig

%description
alternatives creates, removes, maintains and displays information about the
symbolic links comprising the alternatives system. The alternatives system
is a reimplementation of the Debian alternatives system. It was rewritten
primarily to remove the dependence on perl; it is intended to be a drop in
replacement for Debian's update-dependencies script.

%package docs
Summary: Doc files, man pages for alternatives

%description docs
Doc files, man pages for alternatives

%prep
# Using autosetup is not feasible
%setup -q -n %{src_name}-%{version}
%patch -p1 -P 0

%build
%make_build alternatives subdirs

%install
%make_install %{?_smp_mflags} \
        MANDIR=%{_mandir} SBINDIR=%{_sbindir}

%find_lang %{src_name}

mkdir -p %{buildroot}/%{_sharedstatedir}/alternatives

%clean
rm -rf %{buildroot}

%files -f %{src_name}.lang
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/alternatives
%{_sbindir}/update-alternatives
%{_sbindir}/alternatives
%dir %{_sharedstatedir}/alternatives

%files docs
%exclude %{_mandir}/*/chkconfig*
%{_mandir}/*/update-alternatives*
%{_mandir}/*/alternatives*
%exclude %{_mandir}/*/ntsysv.8*

%changelog
* Fri Jun 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.32-4
- Enable Obsoletes
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.32-3
- Extended to build for subrelease 91 and above
* Wed Apr 22 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.32-2
- Conflict chkconfig
* Thu Mar 12 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 1.32-1
- Deprecate chkconfig and ntsysv packages. Only package alternatives from now on.
