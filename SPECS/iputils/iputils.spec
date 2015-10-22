Summary:	Programs for basic networking
Name:		iputils
Version:	s20121221
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/inetutils
Group:		Applications/Communications
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.skbuff.net/iputils/%{name}-%{version}.tar.bz2
BuildRequires: libcap-devel openssl-devel gnutls-devel vim-extra git
Requires:		libcap 
Requires:		openssl
Requires:		gnutls
Obsoletes:		inetutils
%define sha1 iputils=4d56d8c75d6a5d58f052e4056e975f01ebab9ba9
%description
The Iputils package contains programs for basic networking.
%prep
%setup -q

%build
make %{?_smp_mflags} 
(
cd ninfod
./configure --prefix=%{_prefix} 
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
install -cp ping6 %{buildroot}%{_bindir}/
install -cp tracepath %{buildroot}%{_bindir}/
install -cp tracepath6 %{buildroot}%{_bindir}/
install -cp ninfod/ninfod %{buildroot}%{_sbindir}/

ln -sf ../bin/ping6 %{buildroot}%{_sbindir}
ln -sf ../bin/tracepath %{buildroot}%{_sbindir}
ln -sf ../bin/tracepath6 %{buildroot}%{_sbindir}

iconv -f ISO88591 -t UTF8 RELNOTES -o RELNOTES.tmp
touch -r RELNOTES RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%doc RELNOTES
%{_sbindir}/*
%{_bindir}/*

%changelog
*	Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.2-1
-	Initial build.	First version
