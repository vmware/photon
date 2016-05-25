Summary: Versatile resource statistics tool
Name:    dstat
Version: 0.7.2
Release: 2%{?dist}
License: GPLv2
URL: http://dag.wiee.rs/home-made/dstat/
Source: %{name}-%{version}.tar.bz2
%define sha1 dstat=10baf061e3d38e1234fb99182fc53509adf07269
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

%description
Dstat gives you detailed selective information in columns and clearly indicates in what magnitude and unit the output is displayed. Less confusion, less mistakes. And most importantly, it makes it very easy to write plugins to collect your own counters and extend in ways you never expected. 

%prep
%setup -q

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/*
%{_bindir}/dstat
%{_datadir}/dstat/

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  0.7.2-2
-	GA - Bump release of all rpms
*	Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
-   Initial build.  First version
