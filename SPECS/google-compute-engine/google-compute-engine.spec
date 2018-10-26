%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Package for Google Compute Engine Linux images
Name:           google-compute-engine
Version:        2.8.4
Release:        2%{?dist}
License:        Apache License 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:        https://github.com/GoogleCloudPlatform/compute-image-packages/archive/compute-image-packages-20180905.tar.gz
%define sha1    compute-image-packages=ef6a31ba42b0f9fcd7187e45bc953ef7df2b231e
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python-setuptools
Requires:       python2-libs
Requires:       python-boto
Obsoletes:      google-daemon

BuildArch:      noarch

%description
Collection of packages installed on Google supported Compute Engine images.

%package -n     python3-%{name}
Summary:        Python3 bindings for Google Compute Engine Linux images package
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-libs
Requires:       python3-boto
Obsoletes:      google-daemon

%description -n python3-%{name}
Python 3 version bindings for %{name}

%package -n google-compute-engine-services
Summary:        Service files for compute engine package
#Requires:       %{name}=%{version}-%{release}

%description -n google-compute-engine-services
Collection of service files for packages installed on Google supported Compute Engine images.

%prep
%setup -q -n compute-image-packages-20180905
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
mv %{buildroot}/%{_bindir}/google_metadata_script_runner %{buildroot}/%{_bindir}/google_metadata_script_runner3
mv %{buildroot}/%{_bindir}/google_network_daemon %{buildroot}/%{_bindir}/google_network_daemon3
mv %{buildroot}/%{_bindir}/optimize_local_ssd %{buildroot}/%{_bindir}/optimize_local_ssd3
mv %{buildroot}/%{_bindir}/set_multiqueue %{buildroot}/%{_bindir}/set_multiqueue3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -d %{buildroot}%{_libdir}/systemd/system
cp google_compute_engine_init/systemd/*.service %{buildroot}%{_libdir}/systemd/system

%post -n google-compute-engine-services
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-network-daemon

systemctl enable google-accounts-daemon.service
systemctl enable google-clock-skew-daemon.service
systemctl enable google-instance-setup.service
systemctl enable google-network-daemon.service
systemctl enable google-shutdown-scripts.service
systemctl enable google-startup-scripts.service

systemctl start --no-block google-accounts-daemon
systemctl start --no-block google-clock-skew-daemon
systemctl start --no-block google-network-daemon

%postun -n google-compute-engine-services
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-network-daemon

systemctl --no-reload disable google-accounts-daemon.service
systemctl --no-reload disable google-clock-skew-daemon.service
systemctl --no-reload disable google-instance-setup.service
systemctl --no-reload disable google-network-daemon.service
systemctl --no-reload disable google-shutdown-scripts.service
systemctl --no-reload disable google-startup-scripts.service

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/google_accounts_daemon
%{_bindir}/google_clock_skew_daemon
%{_bindir}/google_instance_setup
%{_bindir}/google_metadata_script_runner
%{_bindir}/google_network_daemon
%{_bindir}/optimize_local_ssd
%{_bindir}/set_multiqueue

%files -n python3-google-compute-engine
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/google_accounts_daemon3
%{_bindir}/google_clock_skew_daemon3
%{_bindir}/google_instance_setup3
%{_bindir}/google_metadata_script_runner3
%{_bindir}/google_network_daemon3
%{_bindir}/optimize_local_ssd3
%{_bindir}/set_multiqueue3

%files -n google-compute-engine-services
%defattr(-,root,root)
%{_libdir}/systemd/system/*.service

%changelog
*   Thu Oct 25 2018 Tapas Kundu <tkundu@vmware.com> 2.8.4-2
-   Corrected the source tar name
*   Wed Oct 24 2018 Anish Swaminathan <anishs@vmware.com>  2.8.4-1
-   Rename version to 2.8.4
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com>  20180905-1
-   Upgrade to 20180905
*   Wed Aug 23 2017 Anish Swaminathan <anishs@vmware.com> 20170426-3
-   Remove boto configuration from instance setup
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 20170426-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Fri Apr 28 2017 Anish Swaminathan <anishs@vmware.com> 20170426-1
-   Initial packaging for Photon

