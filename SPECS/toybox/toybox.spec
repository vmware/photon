Name:           toybox
Version:        0.7.3
Release:        3%{?dist}
License:        BSD
Summary:        Common Linux command line utilities in a single executable
Url:            http://landley.net/toybox/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://landley.net/toybox/downloads/%{name}-%{version}.tar.gz
%define sha1 toybox=f3d9f5396a210fb2ad7d6309acb237751c50812f
Source1:	config-%{version}
%description
Toybox combines common Linux command line utilities together into a single
BSD-licensed executable that's simple, small, fast, reasonably
standards-compliant, and powerful enough to turn Android into a development
environment.

%prep
%setup -q -n toybox-%{version}

%build
cp %{SOURCE1} .config
NOSTRIP=1 make CFLAGS="-Wall -Wundef -Wno-char-subscripts -Werror=implicit-function-declaration -g"

%install
PREFIX=%{buildroot} make install
chmod 755 %{buildroot}/bin/toybox

%check
# Do not run all tests, skip losetup
# make tests
sed -i "s/^  if \[ \$# -ne 0 \]/  if false; /" scripts/test.sh
pushd tests
tests_to_run=`ls *.test | sed 's/.test//;/losetup/d'`
popd
tests_to_run=`echo  $tests_to_run | sed -e 's/pkill//g'`
./scripts/test.sh $tests_to_run

%files
%defattr(-,root,root)
%doc README LICENSE
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*

%changelog
*   Thu Jun 01 2017 Chang Lee <changlee@vmware.com> 0.7.3-3
-   Remove pkill test in %check
*   Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.3-2
-   Ensure debuginfo
*   Thu Apr 20 2017 Fabio Rapposelli <fabio@vmware.com> 0.7.3-1
-   Initial build.  First version
