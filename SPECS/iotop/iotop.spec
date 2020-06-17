%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.
Name:		iotop
Version:	0.6
Release:	6%{?dist}
License:	GPLv2
URL:		http://guichaz.free.fr/iotop/
Group:		System/Monitoring
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://guichaz.free.fr/iotop/files/%{name}-%{version}.tar.gz
%define sha1 iotop=71a0e7043d83673a40d7ddc57f5b50adab7fff2a
Patch0:        python3_compatibility_fix.patch
BuildRequires: python3 python3-libs
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
 Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.

%prep
%setup -q
%patch0 -p1
%build

python3 setup.py build
%install

#!/bin/bash
# http://bugs.python.org/issue644744
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --record="INSTALLED_FILES"
# 'brp-compress' gzips the man pages without distutils knowing... fix this
sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.gz@g' "INSTALLED_FILES"
sed -i -e 's@\(.\+\)\.py$@\1.py*@' \
       -e '/.\+\.pyc$/d' \
       "INSTALLED_FILES"
echo "%dir %{python3_sitelib}/iotop" >> INSTALLED_FILES

%clean
rm -rf %{buildroot}/*

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc COPYING NEWS THANKS
%{python3_sitelib}/*

%changelog
*	Fri Dec 06 2019 Tapas Kundu <tkundu@vmware.com> 0.6-6
-	Build with python3
-	Mass removal python2
*	Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-5
-	Use python2 explicitly
*	Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-4
-	Add python2 to Requires
*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-3
-	Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
-	GA - Bump release of all rpms
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6-1
-	Initial build.	First version
