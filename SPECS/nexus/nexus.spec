%define debug_package %{nil}
Summary:       An repository manager allows to store and retrieve build artifacts.
Name:          nexus
Version:       3.13.0
Release:       1%{?dist}
License:       Eclipse Public License 1.0
URL:           https://www.sonatype.com/nexus-repository-oss
Group:         Utilities/System 
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://github.com/sonatype/nexus-public/archive/%{name}-%{version}-01.tar.gz
%define sha1   nexus=eed15d21c5bfaef15dd845d3c8ec11ce44bcaa46
Patch0:        nexus-fix-surefire.patch
Source1:       nexus.service
BuildRequires: apache-maven
BuildRequires: openjdk8
BuildRequires: unzip

%description
Nexus brings you such a repository for your company. 
So you can host your own repositories, but also use 
Nexus as a proxy for public repositories.

%prep
%setup -q -n %{name}-public-release-%{version}-01
%patch0 -p1

%build
./mvnw clean install

%install
unzip -d target assemblies/nexus-base-template/target/nexus-base-template-*.zip
install -v -m755 -d %{buildroot}/usr/share/%{name}
install -v -m755 -d %{buildroot}/usr/share/doc/%{name}-%{version}
install -vd %{buildroot}%{_libdir}/systemd/system/
cd target
cp -r sonatype-work/ nexus-base-template-%{version}-01/ %{buildroot}/usr/share/%{name}/
cp nexus-base-template-%{version}-01/NOTICE.txt nexus-base-template-%{version}-01/OSS-LICENSE.txt %{buildroot}/usr/share/doc/%{name}-%{version}
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group %{name} >/dev/null || groupadd -r %{name}
    getent passwd %{name} >/dev/null || useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
            -c "Nexus" %{name}
fi

%post
%systemd_post nexus.service

%preun
%systemd_preun nexus.service

%postun
%systemd_postun_with_restart nexus.service
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel %{name}
    groupdel %{name}
fi

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/*
%{_datadir}/%{name}/*
%{_libdir}/systemd/system/%{name}.service
%exclude %{_datadir}/%{name}/bin/%{name}.bat
%exclude %{_datadir}/%{name}/bin/setenv.bat

%changelog
*    Thu Sep 27 2018 Keerthana K <keerthanak@vmware.com> 3.13.0-01-1
-    Initial build. First Version
