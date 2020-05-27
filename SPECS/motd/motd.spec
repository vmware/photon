%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define commit0 a152954dcf0583a6efd1af31c42f9e27e6a15bea

Summary:        Message of the Day
Name:           motd
Version:        0.1.3
Release:        5%{?dist}
License:        GPLv3
URL:            http://github.com/rtnpro/fedora-motd
Source0:        https://github.com/rtnpro/motdgen/archive/motdgen-a152954.tar.gz
%define sha1    motdgen-a152954.tar.gz=fd0b535df54515ce5f56933e53b0ed73c77d1137
Patch0:         strip-dnf.patch

BuildArch: noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       Linux-PAM
Requires:       systemd
Requires:       python3
Requires:       /bin/grep

%description
Generates Dynamic MOTD.

%prep
%setup -q -n motdgen-%{commit0}
%patch0 -p1

%build
python3 setup.py build

%install
python3 setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

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

%changelog
*   Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.3-5
-   Add python3-setuptools and python3-xml Buildrequires.
*   Mon Jun 12 2017 Bo Gan <ganb@vmware.com> 0.1.3-4
-   Add grep dependency
*   Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.3-3
-   Upgraded to python3.
*   Sun Apr 30 2017 Bo Gan <ganb@vmware.com> 0.1.3-2
-   Do not write to stdout in triggers
*   Mon Apr 17 2017 Bo Gan <ganb@vmware.com> 0.1.3-1
-   Initial packaging for motd
