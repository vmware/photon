%global build_if %{photon_subrelease} >= 91

Summary:        A project for generating C bindings from Rust code
Name:           cbindgen
Version:        0.29.2
Release:        2%{?dist}
Group:          Development/Languages/Rust
URL:            https://github.com/mozilla/cbindgen
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-registry-%{version}-1%{?dist}.tar.gz

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  rust

%description
A project for generating C bindings from Rust code

%prep
%autosetup -a0 -a1
mkdir -p $HOME/.cargo/
mv registry $HOME/.cargo/

%build
cargo build --offline --release

%install
install -D -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.29.2-2
- Extended to build for subrelease 91 and above
* Mon Feb 16 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.29.2-1
- Initial version
