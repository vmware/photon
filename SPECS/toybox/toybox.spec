Name:           toybox
Version:        0.7.3
Release:        1%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%package symlinks
Summary:    symlinks for %{name}

%description symlinks
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

This package contains compat symlinks.


%prep
%setup -q -n toybox-%{version}

%build
make defconfig toybox

%install
PREFIX=%{buildroot} make install
chmod 755 %{buildroot}/bin/toybox

%files
%defattr(-,root,root)
/bin/toybox

# Note: README and LICENSE are in symlinks to avoid empty rpm ...
%files symlinks
%defattr(-,root,root)
%doc README LICENSE
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%exclude /bin/toybox

%changelog
*   Thu Apr 20 2017 Fabio Rapposelli <fabio@vmware.com> 0.7.3-1
-   Initial build.  First version
