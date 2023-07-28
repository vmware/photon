Summary:    Versatile resource statistics tool
Name:       dstat
Version:    0.7.4
Release:    2%{?dist}
License:    GPLv2
URL:        https://github.com/dstat-real/dstat
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

Source0: https://github.com/dstat-real/dstat/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d100223887ebd83d0fd1259436f39419a85df9002556abcfc8e4195aa63be73d85707dcd5c4fb56a979b29131485dce6e97c177fbfca08dc50bd0f92b15cc6f5

Patch0: 0001-dstat-use-collections.abc.Sequence.patch

Requires: python3
Requires: python3-curses

%description
Dstat gives you detailed selective information in columns and clearly
indicates in what magnitude and unit the output is displayed.
Less confusion, less mistakes. And most importantly, it makes it very
easy to write plugins to collect your own counters and extend in ways
you never expected.

%prep
%autosetup -p1

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/*
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Fri Jul 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.7.4-2
- Fix collections import in dstat
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.4-1
- Automatic Version Bump
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.2-2
- GA - Bump release of all rpms
* Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
- Initial build. First version
