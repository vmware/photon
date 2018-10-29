Summary:          Programs for basic networking
Name:             iputils
Version:          20180629
Release:          1%{?dist}
License:          BSD-3 and GPLv2+
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           VMware, Inc.
Distribution:     Photon
#https://github.com/iputils/iputils/archive/s20180629.tar.gz
Source0:          %{name}-s%{version}.tar.gz
BuildRequires:    libcap-devel libgcrypt-devel
Requires:         libcap 
Requires:         libgcrypt
Obsoletes:        inetutils
%define sha1 iputils=353df20691bf027ad35fcaaf6894b122c39d8f2d
%description
The Iputils package contains programs for basic networking.
%prep
%setup -q -n %{name}-s%{version}

%build
if [ %{_host} != %{_build} -a %{_target} = "i686-linux" ]; then
export CC=i686-linux-gnu-gcc
export CXX=i686-linux-gnu-g++
export AR=i686-linux-gnu-ar
export AS=i686-linux-gnu-as
export RANLIB=i686-linux-gnu-ranlib
export LD=i686-linux-gnu-ld
export STRIP=i686-linux-gnu-strip
fi
make %{?_smp_mflags} USE_IDN=no USE_GCRYPT=yes
(
cd ninfod
%configure --target=%{_target}
make %{?_smp_mflags} 
)
#make html
#make man

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}

install -c clockdiff %{buildroot}%{_sbindir}/
install -cp arping %{buildroot}%{_sbindir}/
install -cp ping %{buildroot}%{_bindir}/
install -cp rdisc %{buildroot}%{_sbindir}/
install -cp tracepath %{buildroot}%{_bindir}/
install -cp traceroute6 %{buildroot}%{_bindir}/
install -cp ninfod/ninfod %{buildroot}%{_sbindir}/

ln -sf ../bin/tracepath %{buildroot}%{_sbindir}
ln -sf ../bin/traceroute6 %{buildroot}%{_sbindir}

iconv -f ISO88591 -t UTF8 RELNOTES.old -o RELNOTES.tmp
touch -r RELNOTES.old RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES.old

%files
%defattr(-,root,root)
%doc RELNOTES.old
%{_sbindir}/rdisc
%{_sbindir}/ninfod
%{_sbindir}/tracepath
%{_sbindir}/traceroute6
%{_bindir}/tracepath
%{_bindir}/traceroute6
%caps(cap_net_raw=p) %{_sbindir}/clockdiff
%caps(cap_net_raw=p) %{_sbindir}/arping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping

%changelog
*   Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 20180629-1
-   Updated to version 20180629
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 20151218-4
-   Remove openssl and gnutls deps
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20151218-3
-   GA - Bump release of all rpms
*   Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 20151218-2
-   Fixing permissions for binaries
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 20151218-1
-   Updated to version 2.4.18
*   Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 20121221-1
-   Initial build.    First version
