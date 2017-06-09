%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity. 
Name:		iotop  
Version:	0.6
Release:	4%{?dist}
License:	GPLv2 
URL:		http://guichaz.free.fr/iotop/
Group:		System/Monitoring
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://guichaz.free.fr/iotop/files/%{name}-%{version}.tar.gz
%define sha1 iotop=71a0e7043d83673a40d7ddc57f5b50adab7fff2a
BuildRequires: python2 python2-libs
BuildArch:      noarch

%description
 Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity. 

%prep
%setup -q
%build

python2 setup.py build
%install

#!/bin/bash
# http://bugs.python.org/issue644744
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot} --record="INSTALLED_FILES"
# 'brp-compress' gzips the man pages without distutils knowing... fix this
sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.gz@g' "INSTALLED_FILES"
sed -i -e 's@\(.\+\)\.py$@\1.py*@' \
       -e '/.\+\.pyc$/d' \
       "INSTALLED_FILES"
echo "%dir %{python2_sitelib}/iotop" >> INSTALLED_FILES

%clean
rm -rf %{buildroot}/*
 
%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc COPYING NEWS THANKS


%changelog
*	Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-4
-	Use python2 explicitly
*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-3
-	Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
-	GA - Bump release of all rpms
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6-1
-	Initial build.	First version
