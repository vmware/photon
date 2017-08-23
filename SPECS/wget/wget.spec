Summary:        A network utility to retrieve files from the Web
Name:           wget
Version:        1.19.1
Release:        2%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/wget/wget.html
Group:          System Environment/NetworkingPrograms
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha1    wget=cde25e99c144191644406793cbd1c69c102c6970
Requires:       openssl
BuildRequires:  openssl-devel
%if %{with_check}
BuildRequires:  perl
%endif

%description
The Wget package contains a utility useful for non-interactive 
downloading of files from the Web.
%prep
%setup -q

%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --with-ssl=openssl 
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc
cat >> %{buildroot}/etc/wgetrc <<-EOF
#   default root certs location
    ca_certificate=/etc/pki/tls/certs/ca-bundle.crt
EOF
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
export PERL_MM_USE_DEFAULT=1
cpan HTTP::Daemon
make  %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%changelog
*   Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.19.1-2
-   Install HTTP::Daemon perl module for the tests to pass.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-1
-   Updated to version 1.19.1.
*   Tue Nov 29 2016 Anish Swaminathan <anishs@vmware.com>  1.18-1
-   Upgrade wget versions - fixes CVE-2016-7098
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.17.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.17.1-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.17.1-1
-   Upgrade version
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
-   Initial build.  First version
