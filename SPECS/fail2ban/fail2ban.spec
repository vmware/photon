Summary:        Daemon to ban hosts that cause multiple authentication errors
Name:           fail2ban
Version:        1.0.2
Release:        5%{?dist}
Group:          Productivity/Networking/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://fail2ban.sourceforge.net

Source0: https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: 00-fail2ban-systemd.conf

Source2: license.txt
%include %{SOURCE2}

Patch0: 0001-Set-proper-config-path-in-include-section.patch
Patch1: 0001-Replace-2to3-binary-name-with-2to3-3.11.patch

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-tools
BuildRequires: sqlite-devel
BuildRequires: systemd-devel

%if 0%{?with_check}
BuildRequires: python3-systemd
%endif

Requires: systemd
Requires: python3-systemd
Requires: nftables
Requires: perl
Requires: whois
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# Default components
Requires: %{name} = %{version}-%{release}
Requires: %{name}-sendmail = %{version}-%{release}
Requires: %{name}-systemd = %{version}-%{release}

%description
Fail2Ban scans log files and bans IP addresses that makes too many password
failures. It updates firewall rules to reject the IP address. These rules can
be defined by the user. Fail2Ban can read multiple log files such as sshd or
Apache web server ones.

The main package contains the core server components for Fail2Ban with minimal
dependencies.  You can install this directly if you want to have a small
installation and know what you are doing.

%package devel
Summary:  Fail2Ban testcases
Group:    Productivity/Networking/Security
Requires: %{name} = %{version}-%{release}

%description devel
This package contains Fail2Ban's testscases and scripts.

%package mail
Summary:  Mail actions for Fail2Ban
Group:    Productivity/Networking/Security
Requires: %{name} = %{version}-%{release}
Requires: sendmail

%description mail
This package installs Fail2Ban's mail actions.  These are an alternative
to the default sendmail actions.

%package sendmail
Summary:  Sendmail actions for Fail2Ban
Group:    Productivity/Networking/Security
Requires: %{name} = %{version}-%{release}
Requires: sendmail

%description sendmail
This package installs Fail2Ban's sendmail actions.  This is the default
mail actions for Fail2Ban.

%package systemd
Summary:  Systemd journal configuration for Fail2Ban
Group:    Productivity/Networking/Security
Requires: %{name} = %{version}-%{release}

%description systemd
This package configures Fail2Ban to use the systemd journal for its log input
by default.

%prep
%autosetup -p1

%build
bash ./%{name}-2to3
%{py3_build}

%install
%{py3_install}
ln -sfv python3 %{buildroot}%{_bindir}/%{name}-python

mkdir -p %{buildroot}%{_unitdir} \
         %{buildroot}%{_tmpfilesdir} \
         %{buildroot}%{_mandir}/man{1,5} \
         %{buildroot}%{_sysconfdir}/logrotate.d

cp -p build/%{name}.service %{buildroot}%{_unitdir}

install -p -m 644 man/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 man/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 files/%{name}-logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -d -m 0755 %{buildroot}/run/%{name}/
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}/
install -p -m 0644 files/%{name}-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Remove non-Linux actions, config files for other distros, installed doc
rm -rf %{buildroot}%{_sysconfdir}/%{name}/action.d/*ipfw.conf \
       %{buildroot}%{_sysconfdir}/%{name}/action.d/{ipfilter,pf,ufw}.conf \
       %{buildroot}%{_sysconfdir}/%{name}/action.d/osx-*.conf \
       %{buildroot}%{_sysconfdir}/%{name}/paths-{arch,debian,freebsd,opensuse,osx}.conf \
       %{buildroot}%{_docdir}/%{name}

# systemd journal configuration
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/jail.d/

%if 0%{?with_check}
%check
%{python3} bin/%{name}-testcases --verbosity=2 --no-network
%endif

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}-client
%{_bindir}/%{name}-python
%{_bindir}/%{name}-regex
%{_bindir}/%{name}-server
%{python3_sitelib}/*
%exclude %{python3_sitelib}/%{name}/tests
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-client.1*
%{_mandir}/man1/%{name}-python.1*
%{_mandir}/man1/%{name}-regex.1*
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man5/*.5*
%config(noreplace) %{_sysconfdir}/%{name}/filter.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/smtp.py
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/filter.d/ignorecommands/apache-fakegooglebot
%config(noreplace) %{_sysconfdir}/%{name}/jail.conf
%config(noreplace) %{_sysconfdir}/%{name}/paths-*.conf
%exclude %{_sysconfdir}/%{name}/filter.d/sendmail-*.conf
%exclude %{_sysconfdir}/%{name}/action.d/complain.conf
%exclude %{_sysconfdir}/%{name}/action.d/hostsdeny.conf
%exclude %{_sysconfdir}/%{name}/action.d/mail.conf
%exclude %{_sysconfdir}/%{name}/action.d/mail-buffered.conf
%exclude %{_sysconfdir}/%{name}/action.d/mail-whois.conf
%exclude %{_sysconfdir}/%{name}/action.d/mail-whois-lines.conf
%exclude %{_sysconfdir}/%{name}/action.d/sendmail-*.conf
%exclude %{_sysconfdir}/%{name}/jail.d/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_tmpfilesdir}/%{name}.conf
%dir %{_sharedstatedir}/%{name}
%dir /run/%{name}/

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-testcases
%{_mandir}/man1/%{name}-testcases.1*
%{python3_sitelib}/%{name}/tests

%files mail
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/action.d/complain.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/mail.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/mail-buffered.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/mail-whois.conf
%config(noreplace) %{_sysconfdir}/%{name}/action.d/mail-whois-lines.conf

%files sendmail
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/action.d/sendmail-*.conf
%config(noreplace) %{_sysconfdir}/%{name}/filter.d/sendmail-*.conf

%files systemd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/jail.d/00-%{name}-systemd.conf

%changelog
* Wed May 07 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.2-5
- Build without tcp_wrappers
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.0.2-4
- Release bump for SRP compliance
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.0.2-3
- Bump version as a part of sqlite upgrade to v3.43.2
* Tue Jan 16 2024 Nitesh Kumar <kunitesh@vmware.com> 1.0.2-2
- Version bump up to use sendmail v8.18.0.2
* Tue Feb 14 2023 Nitesh Kumar <kunitesh@vmware.com> 1.0.2-1
- Initial version
