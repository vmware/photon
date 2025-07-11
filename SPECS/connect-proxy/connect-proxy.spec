Name:           connect-proxy
Summary:        SSH Proxy command helper
Version:        1.105
Release:        2%{?dist}
URL:            https://github.com/gotoh/ssh-connect
Group:          Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/gotoh/ssh-connect/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: socklen.patch

Requires: openssh-clients

BuildRequires: gcc
BuildRequires: make

%description
connect-proxy is the simple relaying command to make network connection via
SOCKS and https proxy. It is mainly intended to be used as proxy command
of OpenSSH. You can make SSH session beyond the firewall with this command.
Features of connect-proxy are:
* Supports SOCKS (version 4/4a/5) and https CONNECT method.
* Supports NO-AUTH and USERPASS authentication of SOCKS
* Partially supports telnet proxy (experimental).
* You can input password from tty, ssh-askpass or environment variable.
* Simple and general program independent from OpenSSH.
* You can also relay local socket stream instead of standard I/O.

%prep
%autosetup -p1 -n ssh-connect-%{version}

%build
%make_build

%install
install -vDm 0755 connect %{buildroot}%{_bindir}/connect-proxy

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Thu Jul 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.105-2
- Cleanup spec
* Fri Apr 11 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.105-1
- Initial build
