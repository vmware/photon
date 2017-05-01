%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_version: %define python_version %(%{__python} -c "import sys ; print sys.version[:3]")}

%define commit0 a152954dcf0583a6efd1af31c42f9e27e6a15bea

Summary:	Message of the Day
Name:		motd
Version:	0.1.3
Release:	2%{?dist}
License:	GPLv3
URL:		http://github.com/rtnpro/fedora-motd
Source0:	https://github.com/rtnpro/motdgen/archive/motdgen-a152954.tar.gz
%define sha1 motdgen-a152954.tar.gz=fd0b535df54515ce5f56933e53b0ed73c77d1137
Patch0:		strip-dnf.patch

BuildArchitectures: noarch

BuildRequires:	python2-devel
BuildRequires:	python-setuptools

Requires:	Linux-PAM
Requires:	systemd
Requires:	python2

%description
Generates Dynamic MOTD.

%prep
%setup -q -n motdgen-%{commit0}
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
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
%{python_sitelib}/motdgen-%{version}-py%{python_version}.egg-info/
%{_sysconfdir}/pam.d/motdgen
%{_sysconfdir}/motdgen.d
%{_sysconfdir}/profile.d/motdgen.sh
%{_bindir}/motdgen
%{_sysconfdir}/systemd/system/motdgen.service

%changelog
*   Sun Apr 30 2017 Bo Gan <ganb@vmware.com> 0.1.3-2
-   Do not write to stdout in triggers
*   Mon Apr 17 2017 Bo Gan <ganb@vmware.com> 0.1.3-1
-   Initial packaging for motd
