Name:           cpulimit
Version:        1.1
Release:        1%{?dist}
Summary:        CPU Usage Limiter for Linux
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
License:        GPLv2+
URL:            http://cpulimit.sourceforge.net

Source0:        https://telkomuniversity.dl.sourceforge.net/project/cpulimit/cpulimit/cpulimit/%{name}-%{version}.tar.gz
%define sha512  %{name}=dfc111e90ee01f1f5277b5be1e5f9dbccb560dced335207b58b5db2a370013f76dd557dd3f63d9501011f3b34c41e21b5845fc4ac00f3eceac8b1179db1c747b

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
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -Dp -m 755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Tue May 10 2022 Benson Kwok <bkwok@vmware.com> 1.1-1
- Initial build. First version
