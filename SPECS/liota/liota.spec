%define debug_package %{nil}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}


Summary:        Little IoT Agent
Name:           liota
Version:        0.4.1
Release:        2%{?dist}
License:        BSD 2-Clause License.
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/liota
Source0:        https://github.com/vmware/liota/archive/%{name}-%{version}.tar.gz
%define         sha1 liota=c20239309086753e0dcc9cfa5e88e09ce63203f5
Patch0:         fix_for_building_liota_with_pip_gr_10.patch
BuildRequires:  python-pip
BuildRequires:  python-pyOpenSSL
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-mistune
BuildRequires:  python-docutils
BuildRequires:  openssl
BuildRequires:  curl
Requires:       chkconfig
BuildArch:      noarch

%description
Little IoT Agent (liota) is an open source project offering some convenience for IoT solution developers in creating IoT Edge System data orchestration applications. Liota has been generalized to allow, via modules, interaction with any data-center component, over any transport, and for any IoT Edge System. It is easy-to-use and provides enterprise-quality modules for interacting with IoT Solutions.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}/etc/%{name}
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/usr/lib/%{name}/examples
mkdir -p %{buildroot}/usr/lib/%{name}/packages
mkdir -p %{buildroot}/%{python2_sitelib}/%{name}
mkdir -p %{buildroot}/usr/lib/%{name}/packages/liotad

python setup.py install

cp /usr/lib/liota/config/liota.conf %{buildroot}/etc/%{name}/
cp /usr/lib/liota/config/logging.json %{buildroot}/etc/%{name}/
cp /usr/lib/liota/config/README.md %{buildroot}/etc/%{name}/
cp scripts/autostartliota %{buildroot}/etc/init.d/
cp -r packages/liotad/* %{buildroot}/usr/lib/%{name}/packages/
cp -r liota/* %{buildroot}/%{python2_sitelib}/%{name}/
cp -r packages/liotad/* %{buildroot}/usr/lib/%{name}/packages/liotad/

%files
%defattr(-,root,root)
/etc/init.d/autostartliota
/usr/lib/%{name}/
/var/log/%{name}
/etc/%{name}
%{python2_sitelib}/%{name}/

%changelog
*   Tue Sep 11 2018 Tapas Kundu <tkundu@vmware.com> 0.4.1-2
-   Added fix to build with pip greater than version 10.
*   Mon Aug 13 2018 Tapas Kundu <tkundu@vmware.com> 0.4.1-1
-   Initial packaging for Photon
