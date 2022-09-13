Name:           cpulimit
Version:        1.2
Release:        1%{?dist}
Summary:        CPU Usage Limiter for Linux
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/opsengine/cpulimit

Source0:        https://github.com/opsengine/cpulimit/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=50f6ab4dc7bffa09fa475b7554d518ec9d75ac325d7247a964b417feecbe466f61d217347513e6e6d111a43af61077a9c6e92b790c71e51c2e27c90fbfd43b1a

Patch0: fix-include-warning-ifdef-macro-errors.patch

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
install -Dp -m 755 src/%{name} %{buildroot}%{_bindir}/%{name}

%if 0%{?with_check}
%check
cd tests && ./process_iterator_test
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Mon May 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2-1
- Upgrade to v1.2
- Actual tag version is 0.2 but to maintain proper versioning, using 1.2
* Tue May 10 2022 Benson Kwok <bkwok@vmware.com> 1.1-1
- Initial build. First version
