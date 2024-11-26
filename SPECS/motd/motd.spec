%define srcname photon-motdgen

Summary:        Message of the Day
Name:           motd
Version:        1.0
Release:        1%{?dist}
License:        GPLv3
URL:            https://github-vcf.devops.broadcom.net/vcf/photon-motdgen
Group:          Applications/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github-vcf.devops.broadcom.net/vcf/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=031d2209e0a582bab9457cf82e80d920b2b121eab9a685dee54aaa0e4556598b949462e4e1fba6342dbbef22231ba29cd9c66d72139a0ed727b093d75eed5004

Source1: %{name}.conf

BuildArch: noarch

BuildRequires: make
BuildRequires: coreutils
BuildRequires: systemd-devel

Requires: bash
Requires: Linux-PAM
Requires: systemd

%description
Generates Dynamic MOTD.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%make_build

%install
%make_install %{?_smp_mflags}
# SELinux: let systemd create our runtime directory and label it properly.
install -D -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/motd.conf

#shadow is providing /etc/pam.d/sshd with (noreplace)

%triggerin -- shadow
[ $1 -eq 1 ] && [ $2 -eq 1 ] || exit 0
echo "detected install of motd/shadow, patching /etc/pam.d/sshd" >&2
grep -q '^\s*session\s*include\s*motdgen.*$' %{_sysconfdir}/pam.d/sshd \
    || echo "session include motdgen" >> %{_sysconfdir}/pam.d/sshd

%triggerun -- shadow
[ $1 -eq 0 ] && [ $2 -eq 1 ] || exit 0
# $1 $2
# 0  1  motd is being uninstalled, shadow is installed
echo "detected uninstall of motd/shadow, reverting /etc/pam.d/sshd" >&2
sed -i '/^\s*session\s*include\s*motdgen.*$/d' \
    %{_sysconfdir}/pam.d/sshd || exit 0

%postun
[ $1 -eq 0 ] || exit 0
rm -rf %{_rundir}/motdgen

%files
%defattr(-,root,root)
%{_sysconfdir}/pam.d/motdgen
%{_sysconfdir}/motdgen.d
%{_sysconfdir}/profile.d/motdgen.sh
%{_bindir}/motdgen
%{_unitdir}/motdgen.service
%{_unitdir}/motdgen.timer
%{_tmpfilesdir}/motd.conf

%changelog
* Tue Nov 26 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.0-1
- Upgrade to v1.0
- Switch to photon-motdgen
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.1.3-7
- Update release to compile with python 3.11
* Thu Apr 30 2020 Alexey Makhalov <amakhalov@vmware.com> 0.1.3-6
- Systemd to generate runtime directory.
* Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.3-5
- Add python3-setuptools and python3-xml Buildrequires.
* Mon Jun 12 2017 Bo Gan <ganb@vmware.com> 0.1.3-4
- Add grep dependency
* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.3-3
- Upgraded to python3.
* Sun Apr 30 2017 Bo Gan <ganb@vmware.com> 0.1.3-2
- Do not write to stdout in triggers
* Mon Apr 17 2017 Bo Gan <ganb@vmware.com> 0.1.3-1
- Initial packaging for motd
