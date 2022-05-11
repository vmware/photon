Name:           cpulimit
Version:        1.1	
Release:        1%{?dist}
Summary:        CPU Usage Limiter for Linux
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
License:        GPLv2+
URL:            http://cpulimit.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{name}/%{name}-%{version}.tar.gz
%define sha1    %{name}=9f020c22d633e3f6289c69844bd7136c1f2704f1
BuildRequires:  glibc-devel
Requires:       glibc

%description
cpulimit is a simple program which attempts to limit the CPU usage of a process
(expressed in percentage, not in CPU time). This is useful to control batch
jobs, when you don't want them to eat too much CPU. It does not act on the nice
value or other scheduling priority stuff, but on the real CPU usage. Also, it
is able to adapt itself to the overall system load, dynamically and quickly.

%prep
%autosetup -p1


%build
gcc $RPM_OPT_FLAGS -lrt -o cpulimit cpulimit.c


%install
rm -rf %{buildroot}
install -Dp -m 755 %{name} %{buildroot}/%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
add %defattr(-,root,root)
%{_bindir}/cpulimit

%changelog
*   Tue May 10 2022 Benson Kwok <bkwok@vmware.com> 1.1-1
-   Initial build. First version
