%global debug_package %{nil}
Summary:        provides the XML-XCB protocol descriptions.
Name:           xcb-proto
Version:        1.15.2
Release:        2%{?dist}
URL:            http://xcb.freedesktop.org/
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.gz
%define sha512  xcb-proto=4aaf4886dbbb465ec9d123beca2db616f4690f76297df7f85a2cb6afeea114e7ee08995268821b090226a55109c93676f134840065b448180a5d61d8d95095b0

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
Requires:       python3

%description
The xcb-proto package provides the XML-XCB protocol descriptions that libxcb uses to generate the majority of its code and API.

%prep
%autosetup -p1

%build
%configure
%make_build

%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_prefix}/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.15.2-2
- Release bump for SRP compliance
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.15.2-1
- Upgrade to 1.15.2
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.11-1
- initial version
