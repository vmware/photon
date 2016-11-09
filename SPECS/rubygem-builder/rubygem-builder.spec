%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary: Builders for MarkUp
Name: rubygem-builder
Version: 3.2.2
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://onestepback.org
Source0: http://rubygems.org/gems/builder-%{version}.gem
%define sha1 builder=0ee99b207f9994864c2a21ce24be26eddafee7f1
Source1:  https://get.rvm.io/rvm-installer
%define sha1 rvm-installer=cf0184a1fc3c0854da5acc1134fac150461d7360
BuildRequires: ruby
Requires: ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%setup -q -c -T
chmod +x  %{SOURCE1}
cp %{SOURCE1} .
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
./rvm-installer
pushd /usr/src/photon/BUILDROOT/rubygem-builder-%{version}-%{release}.x86_64/usr/lib/ruby/gems/2.3.0/gems/builder-%{version}/
export PATH=$PATH:/usr/local/rvm/bin
rake test
popd

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.2.2-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.2-2
-	GA - Bump release of all rpms
* Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.2.2-1
- Initial build
