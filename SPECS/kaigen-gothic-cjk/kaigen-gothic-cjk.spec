%global fontdir /usr/share/fonts/
Summary:	Kaigen-Gothic CJK Fonts
Name:		kaigen-gothic-cjk
Version:	1.002
Release:	2%{?dist}
License:	OFL
URL:		https://github.com/minjiex/kaigen-gothic
Source:		%{name}-%{version}.tar.gz
%define sha1 kaigen-gothic-cjk=2118f1726f74cd3f3a4df8359780ebe5eaa6a44d
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:	noarch

%description
Kaigen-gothic is a set of truetype fonts derive from Source Han Sans - an open
source Pan-CJK font (intended to support the characters necessary to render or
display text in Simplified Chinese, Traditional Chinese, Japanese, and Korean).

%prep
%setup -q -n %{name}-%{version}

%build

%install
install -m 0755 -d %{buildroot}%{fontdir}/truetype
install -m 0644 -p *.ttf %{buildroot}%{fontdir}/truetype

%files
/usr/share/fonts/truetype/*.ttf

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1.002-2
-	GA - Bump release of all rpms
*  Fri May 20 2016 Anish Swaminathan <anishs@vmware.com> 1.002-1
-  Initial version
