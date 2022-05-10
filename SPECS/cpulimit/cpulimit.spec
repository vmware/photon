Name:		cpulimit
Version:        1.1	
Release:	1%{?dist}
Summary:	CPU Usage Limiter for Linux

Group:		Applications/System
License:	GPLv2+
URL:		http://cpulimit.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/%{name}/%{name}/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
cpulimit is a simple program which attempts to limit the CPU usage of a process
(expressed in percentage, not in CPU time). This is useful to control batch
jobs, when you don't want them to eat too much CPU. It does not act on the nice
value or other scheduling priority stuff, but on the real CPU usage. Also, it
is able to adapt itself to the overall system load, dynamically and quickly.

%prep
%setup -q


%build
gcc $RPM_OPT_FLAGS -lrt -o cpulimit cpulimit.c


%install
rm -rf $RPM_BUILD_ROOT
install -Dp -m 755 cpulimit $RPM_BUILD_ROOT/%{_bindir}/cpulimit

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/cpulimit

%changelog
*   Tue May 10 2022 Benson Kwok <bkwok@vmware.com> 0.2-1
-   Initial build. First version
