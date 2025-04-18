%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name sigdump

Name:           rubygem-sigdump
Version:        0.2.5
Release:        2%{?dist}
Summary:        signal handler which dumps backtrace of running threads
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/sigdump-%{version}.gem
%define sha512 %{gem_name}=2400403768f4606cb21a3fc34b4630800846ef5ad4c06f1bfca3b04fb62208bfd48a53f1f090b8c65858b49d1bf594c42f555c2f997534129793773c837cfa73

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires:       ruby

%description
Setup signal handler which dumps backtrace of running threads and number
of allocated objects per class. Require 'sigdump/setup', send SIGCONT,
and see /tmp/sigdump-<pid>.log.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.2.5-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-1
- Update to version 0.2.5
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.2.4-2
- rebuilt using ruby-2.7.1
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.4-1
- Initial build
