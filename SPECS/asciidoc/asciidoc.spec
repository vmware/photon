Summary:    AsciiDoc is a human readable text document format
Name:       asciidoc
Version:    8.6.9
Release:    1
License:    GPLv2
URL:        http://asciidoc.org/
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://sourceforge.net/projects/asciidoc/files/asciidoc/%{version}/%{name}-%{version}.tar.gz

%description
AsciiDoc is a human readable text document format that can be easily converted to other document formats.

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
/usr/bin/*
/usr/etc/*
/usr/share/man/*

%changelog
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 8.6.9-1
-   Initial build.  First version