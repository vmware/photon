%define commit0 a152954dcf0583a6efd1af31c42f9e27e6a15bea

Summary:        Message of the Day
Name:           motd
Version:        0.1.3
Release:        8%{?dist}
URL:            http://github.com/rtnpro/fedora-motd
Group:          Applications/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/rtnpro/motdgen/archive/motdgen-a152954.tar.gz
%define sha512  motdgen-a152954.tar.gz=784d6fa426c48386a584c7d026a585718a8665a249cae9450073f812b5b4935fa20d4127dcb9c937ac4470b4f19e9349974bf0e4c341d95a162a04438ce98276

Source1: license.txt
%include %{SOURCE1}

Patch0:         strip-dnf.patch

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  systemd-devel

Requires:       Linux-PAM
Requires:       systemd
Requires:       python3
Requires:       /bin/grep

%description
Generates Dynamic MOTD.

%prep
%autosetup -p1 -n motdgen-%{commit0}

%build
%py3_build

%install
python3 setup.py install -O1 --skip-build --install-data=%{_datadir} --root %{buildroot}
# SELinux: let systemd create our runtime directory and label it properly.
mkdir -p %{buildroot}%{_tmpfilesdir}
echo "d /run/motdgen 0755 root root" > %{buildroot}%{_tmpfilesdir}/motd.conf

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
rm -rf %{_localstatedir}/run/motdgen

%files
%doc README.md
%defattr(-,root,root)
%{python3_sitelib}/*
%{_sysconfdir}/pam.d/motdgen
%{_sysconfdir}/motdgen.d
%{_sysconfdir}/profile.d/motdgen.sh
%{_bindir}/motdgen
%{_sysconfdir}/systemd/system/motdgen.service
%{_tmpfilesdir}/motd.conf

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.1.3-8
- Release bump for SRP compliance
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
