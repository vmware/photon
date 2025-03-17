Summary:        Autonomous Mail Processor
Name:           procmail
Version:        3.22
Release:        6%{?dist}
URL:            http://www.procmail.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.ring.gr.jp/archives/net/mail/procmail/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:         procmail-3.22-config.patch
Patch1:         procmail-3.22-CVE-2014-3618.patch
#https://bugs.debian.org/cgi-bin/bugreport.cgi?att=1;bug=876511;filename=formisc.c.patch.txt;msg=10
Patch2:         procmail-3.22-CVE-2017-16844.patch

%description
Procmail is a program for filtering, sorting and storing email. It can be used both on mail clients and mail servers. It can be used to filter out spam, checking for viruses, to send automatic replies, etc.

%prep
%autosetup -p1

%build
sed -i 's/getline/get_line/' src/*.[ch]

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man{1,5}

make install %{?_smp_mflags} \
  BASENAME=%{buildroot}%{_prefix} MANDIR=%{buildroot}%{_mandir}

make install-suid %{?_smp_mflags} \
  BASENAME=%{buildroot}%{_prefix}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.22-6
- Release bump for SRP compliance
* Tue Dec 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.22-5
- Fix CVE-2017-16844
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.22-4
- Ensure non empty debuginfo
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.22-3
- GA - Bump release of all rpms
* Wed Mar 30 2016 Anish Swaminathan <anishs@vmware.com>  3.22-2
- Add patch for CVE-2014-3618
* Mon Nov 02 2015 Divya Thaluru <dthaluru@vmware.com> 3.22-1
- Initial build.  First version
