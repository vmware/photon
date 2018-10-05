%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Package for Google Compute Engine Linux images
Name:           google-compute-engine
Version:        20170426
Release:        3%{?dist}
License:        Apache License 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:        https://github.com/GoogleCloudPlatform/compute-image-packages/archive/compute-image-packages-%{version}.tar.gz
%define sha1    compute-image-packages=6852588ecae9cc39bac7683f1e21f88a5d41e831
Patch0:         remove-boto.patch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python2
Requires:       python-setuptools
Requires:       python2-libs
Obsoletes:      google-daemon

BuildArch:      noarch

%description
Collection of packages installed on Google supported Compute Engine images.

%package -n     python3-%{name}
Summary:        Python3 bindings for Google Compute Engine Linux images package
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-libs
Obsoletes:      google-daemon

%description -n python3-%{name}
Python 3 version bindings for %{name}

%prep
%setup -q -n compute-image-packages-%{version}
%patch0 -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/google_accounts_daemon %{buildroot}/%{_bindir}/google_accounts_daemon3
mv %{buildroot}/%{_bindir}/google_clock_skew_daemon %{buildroot}/%{_bindir}/google_clock_skew_daemon3
mv %{buildroot}/%{_bindir}/google_instance_setup %{buildroot}/%{_bindir}/google_instance_setup3
mv %{buildroot}/%{_bindir}/google_ip_forwarding_daemon %{buildroot}/%{_bindir}/google_ip_forwarding_daemon3
mv %{buildroot}/%{_bindir}/google_metadata_script_runner %{buildroot}/%{_bindir}/google_metadata_script_runner3
mv %{buildroot}/%{_bindir}/google_network_setup %{buildroot}/%{_bindir}/google_network_setup3
mv %{buildroot}/%{_bindir}/optimize_local_ssd %{buildroot}/%{_bindir}/optimize_local_ssd3
mv %{buildroot}/%{_bindir}/set_multiqueue %{buildroot}/%{_bindir}/set_multiqueue3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/google_accounts_daemon
%{_bindir}/google_clock_skew_daemon
%{_bindir}/google_instance_setup
%{_bindir}/google_ip_forwarding_daemon
%{_bindir}/google_metadata_script_runner
%{_bindir}/google_network_setup
%{_bindir}/optimize_local_ssd
%{_bindir}/set_multiqueue

%files -n python3-google-compute-engine
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/google_accounts_daemon3
%{_bindir}/google_clock_skew_daemon3
%{_bindir}/google_instance_setup3
%{_bindir}/google_ip_forwarding_daemon3
%{_bindir}/google_metadata_script_runner3
%{_bindir}/google_network_setup3
%{_bindir}/optimize_local_ssd3
%{_bindir}/set_multiqueue3

%changelog
*   Wed Aug 23 2017 Anish Swaminathan <anishs@vmware.com> 20170426-3
-   Remove boto configuration from instance setup
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 20170426-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri Apr 28 2017 Anish Swaminathan <anishs@vmware.com> 20170426-1
-   Initial packaging for Photon
