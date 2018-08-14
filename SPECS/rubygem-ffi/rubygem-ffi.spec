%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi

Name: rubygem-ffi
Version:        1.9.25
Release:        1%{?dist}
Summary:        Ruby FFI library
Group:          Development/Languages
License:        BSD-2-Clause
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/ffi-%{version}.gem
%define sha1    ffi=86fa011857f977254ccf39f507587310f9ade768
BuildRequires:  ruby > 2.1.0
BuildArch: %{_arch}
Provides: rubygem-ffi = %{version}

%description
Ruby FFI library

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}
%exclude /usr/lib/ruby/gems/2.4.0/gems/ffi-1.9.25/ext/ffi_c/libffi-x86_64-linux/include/ffitarget.h

%changelog
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.9.25-1
-   Initial build
