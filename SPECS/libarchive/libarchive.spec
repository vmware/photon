Summary:    Multi-format archive and compression library
Name:       libarchive
Version:    3.1.2
Release:    1
License:    BSD 2-Clause License
URL:        http://www.libarchive.org/
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz

%description
Multi-format archive and compression library

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/lib/*
/usr/bin/*
/usr/share/man/*
/usr/include/*

%changelog
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 3.1.2-1
-   Initial build.  First version