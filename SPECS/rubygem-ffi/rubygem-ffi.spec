%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi

Name: rubygem-ffi
Version:        1.9.25
Release:        2%{?dist}
Summary:        Ruby FFI library
Group:          Development/Languages
License:        BSD-2-Clause
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/ffi-%{version}.gem
%define sha1    ffi=86fa011857f977254ccf39f507587310f9ade768
BuildRequires:  ruby > 2.1.0

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
%exclude /usr/lib/ruby/gems/2.5.0/gems/ffi-1.9.25/ext/ffi_c/libffi-%{_arch}-linux/include/ffitarget.h

%changelog
*   Tue Jan 08 2019 Sujay G <gsujay@vmware.com> 1.9.25-2
-   Fix build issues (Remove BuildArch, Provides paramater) & Added aarch64 support
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.9.25-1
-   Initial build
