%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name thread_safe

Name: rubygem-thread_safe
Version:        0.3.6
Release:        3%{?dist}
Summary:        Thread safe programming support for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/thread_safe/%{version}
Source0:        https://rubygems.org/downloads/thread_safe-%{version}.gem
%define sha512  thread_safe=a11808576392c068e1cb31faad706be2b1bbfa4837c655c2ab1d5a235b62b25ece62065de6b65bd25496fa827ed89eb0796b90467107df255825e01316ff1805

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

%description
A collection of data structures and utilities to make thread-safe programming in Ruby easier

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.3.6-3
-   Release bump for SRP compliance
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.3.6-2
-   Rebuilt using ruby-2.7.1
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 0.3.6-1
-   Initial build
