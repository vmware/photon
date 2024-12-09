%global debug_package %{nil}

Summary:           The Xorg fonts.
Name:              xorg-fonts
Version:           7.7
Release:           4%{?dist}
URL:               http://www.x.org
Group:             Development/System
Vendor:            VMware, Inc.
Distribution:      Photon

Source0: http://ftp.x.org/pub/individual/font/encodings-1.0.6.tar.gz
%define sha512 encodings-1.0.6.tar.gz=3c05c0a8ffdbcf298441756f97b2fbdc81856b1624eb5631801b7706c4d3a45de53dc48c73348c458f3ec2dc8b7aa26e6481272b21f685d346690b2d9a55ce00

Source1: http://ftp.x.org/pub/individual/font/font-adobe-100dpi-1.0.3.tar.bz2
%define sha512 font-adobe-100dpi-1.0.3.tar.bz2=27ed98dcdbb9c174c7090cdd8fe230f7471d10b5dfc63e092640b5d0fc6ab351bc8ffa9a92bec1755f2780b3d9c1de3ad298c64b70a68b5e6879a8592ef32987

Source2: http://ftp.x.org/pub/individual/font/font-adobe-75dpi-1.0.3.tar.bz2
%define sha512 font-adobe-75dpi-1.0.3.tar.bz2=c0d851df5732e81027e265370751a606c6e4f5eea546d802608988dde02de35fa28238f709f48567191090bf18814f671b1a7f9f0b528d54949b0aa9403f266d

Source3: http://ftp.x.org/pub/individual/font/font-adobe-utopia-100dpi-1.0.4.tar.bz2
%define sha512 font-adobe-utopia-100dpi-1.0.4.tar.bz2=fecb9a9bde99a82787d12779ea579c8696dcce168acd74b478a879ae24d421d5978d5f69da651e8ff3b25dca355960aaa19f69f2bf61e540464887e546a7b94b

Source4: http://ftp.x.org/pub/individual/font/font-adobe-utopia-75dpi-1.0.4.tar.bz2
%define sha512 font-adobe-utopia-75dpi-1.0.4.tar.bz2=c569af760a62b00738be65546364587638e8c46e4a0765013747e9595d51bc0633908c72359e42e7ebf6240fdc6294b51512c0a096a5fe64b2bd300ccbff7b92

Source5: http://ftp.x.org/pub/individual/font/font-adobe-utopia-type1-1.0.4.tar.bz2
%define sha512 font-adobe-utopia-type1-1.0.4.tar.bz2=53ff2ce7b17824a0eed1be6c3e3386e51983389f5623e732ac898c4e08769c8720f6d6b7c75b6455e050ec5dc390376747ca4cdb9f831a218f9dd5ee5edcd0d6

Source6: http://ftp.x.org/pub/individual/font/font-alias-1.0.4.tar.bz2
%define sha512 font-alias-1.0.4.tar.bz2=c67ac2ee344a601fcc09471580214b30c3fd6acc4800702840de44f0733e6d18b3faeec2fa3f4e2314025cc1724d7d6796ebaf620398fe350710182fd2c4b07d

Source7: http://ftp.x.org/pub/individual/font/font-arabic-misc-1.0.3.tar.bz2
%define sha512 font-arabic-misc-1.0.3.tar.bz2=46a416bf888afdb54f5dda6c9a7207dc069d14089ba14b262c60cb9ad427784c46e2a61b32a79f1d745e73ea657bbc36b48aa5d4bbd79f73a2d997b027ddfbc0

Source8: http://ftp.x.org/pub/individual/font/font-bh-100dpi-1.0.3.tar.bz2
%define sha512 font-bh-100dpi-1.0.3.tar.bz2=60532fb3bd25bad08b1db65f96fdd1cdb2ae5fd580729d7851f5b619f1ed6bdef4fec30111ec408cec9ae5e94f92ad9cf214214c01ac684f3a4bd8d43bafd8a2

Source9: http://ftp.x.org/pub/individual/font/font-bh-75dpi-1.0.3.tar.bz2
%define sha512 font-bh-75dpi-1.0.3.tar.bz2=fb19c7fe91b6cc0670b01d5b8165075866ad08796293650d6037d79211ca668decdcc1b3684774907c06073145919655690d78ccdcf2511db38b5879328a9f50

Source10: http://ftp.x.org/pub/individual/font/font-bh-lucidatypewriter-100dpi-1.0.3.tar.bz2
%define sha512 font-bh-lucidatypewriter-100dpi-1.0.3.tar.bz2=1862003c20aa7709ea07487a4326c619e2beb33b7069d644f438d64182b41a06039c69e2867921b4d12939612a4b8e1e1727fd15851aeab9a0361060183e3b0f

Source11: http://ftp.x.org/pub/individual/font/font-bh-lucidatypewriter-75dpi-1.0.3.tar.bz2
%define sha512 font-bh-lucidatypewriter-75dpi-1.0.3.tar.bz2=2bba19c10df8e95f95d59d5fc7c15380c91a5140b0fa490497dbdf78a5574adae06a5566941c8c61e4a9850712fc9ca16974173aeee771f41976f472f0a2de13

Source12: http://ftp.x.org/pub/individual/font/font-bh-ttf-1.0.3.tar.bz2
%define sha512 font-bh-ttf-1.0.3.tar.bz2=36b5b6bbc2894cd90a372e8131281a462b42d503be3e9af8565edbcd954b336690aa86a0b6fb162d865ba71b65669c5b911658c5b820effcea39d086d485be25

Source13: http://ftp.x.org/pub/individual/font/font-bh-type1-1.0.3.tar.bz2
%define sha512 font-bh-type1-1.0.3.tar.bz2=dc6cfe7d78a549ae5368ddd2bb3edc6746648b32e1f22bce87f6adc0845ef4827cd3b2472d0afa17a16a2c384e84f74f1c7d807510798bc69089920fdc5486da

Source14: http://ftp.x.org/pub/individual/font/font-bitstream-100dpi-1.0.3.tar.bz2
%define sha512 font-bitstream-100dpi-1.0.3.tar.bz2=10fd920d46d2cb1b314e8c2f05c202e9ffa74a4e5315f34790eba8bd8fcda865a6932eb712a7538624e69367647bcd6891e7015099e65463aeef772d0ba58bfd

Source15: http://ftp.x.org/pub/individual/font/font-bitstream-75dpi-1.0.3.tar.bz2
%define sha512 font-bitstream-75dpi-1.0.3.tar.bz2=9311a5b0cbe1613aca87fdf7fd9ab263eb1129e3c3eacbce54547f2185e151fb1237128b1b6d39f716f28694a486909564ecc9a0aef061438622d11b5661d650

Source16: http://ftp.x.org/pub/individual/font/font-bitstream-type1-1.0.3.tar.bz2
%define sha512 font-bitstream-type1-1.0.3.tar.bz2=71883f7fc0a68b4fb8ef30b8b8bdfd73ae1194b6d6495abde6c819eef7a91d6365ef1b4cae026d6c3fa7fddecc643b46b7ba1232cec404fcada49a92aaf1af61

Source17: http://ftp.x.org/pub/individual/font/font-cronyx-cyrillic-1.0.3.tar.bz2
%define sha512 font-cronyx-cyrillic-1.0.3.tar.bz2=b926c425644f94548ad831c38573009ae97d207a05c9d8a917018c2518911960280eb3861ae11d99bc8d001fb0dca1967712fb70ba4f413bc9d6ac8ef904b456

Source18: http://ftp.x.org/pub/individual/font/font-cursor-misc-1.0.3.tar.bz2
%define sha512 font-cursor-misc-1.0.3.tar.bz2=7ecb7f1c3c11da8b81fc0ff121fa6c1026b11f6c7878ffd0e4959df036511bc579d6b0552422ce13e26a8d188e3406631d2de55cab6b29bc7fce0416a8cffc83

Source19: http://ftp.x.org/pub/individual/font/font-daewoo-misc-1.0.3.tar.bz2
%define sha512 font-daewoo-misc-1.0.3.tar.bz2=7e97bc580f66a1316e366617d34e1dbefd576b47b9373ef34833aaaf2fdefc50befc2add5f038915db0b45fbdd56b77304a8a980bb72726479d429085c406f06

Source20: http://ftp.x.org/pub/individual/font/font-dec-misc-1.0.3.tar.bz2
%define sha512 font-dec-misc-1.0.3.tar.bz2=af755d51c4c59cdbe5d3dccf37990bc787373958feb984bb037c8d8aba8a0eb410965a3600886b5123d89e85e1ea0498b84dfa384fccbbcbcaf3549b83c839c6

Source21: http://ftp.x.org/pub/individual/font/font-ibm-type1-1.0.3.tar.bz2
%define sha512 font-ibm-type1-1.0.3.tar.bz2=cbd179522c936c4f956ff1fbdc48fc3a55990083b4f858c938c6a54c8526641b4f25eb3a6795d774630b75a0f4fbdf9c16e861e88b2cd95f04c524f95d40f90f

Source22: http://ftp.x.org/pub/individual/font/font-isas-misc-1.0.3.tar.bz2
%define sha512 font-isas-misc-1.0.3.tar.bz2=be6fb1d2c53550a462d1ab010fa7ac913990e83a22d4580c93b8f1f087aa6caa0e46bc87debca2b13b10e5611bd2fe7f6b4240367fb24f59b37f68ffb0e2586b

Source23: http://ftp.x.org/pub/individual/font/font-jis-misc-1.0.3.tar.bz2
%define sha512 font-jis-misc-1.0.3.tar.bz2=3ce4c96d54440045e84f54f7d790e350c05b0c56a72491941f2cd9ed7e2d1735ff4b41667501cf08d5d81ee19c9de6d43f88a8b59a3c5c55de9fb1696cae208c

Source24: http://ftp.x.org/pub/individual/font/font-micro-misc-1.0.3.tar.bz2
%define sha512 font-micro-misc-1.0.3.tar.bz2=7a546432225c22ae0aacf9ce88b617a7d1d6678ee1f5eb4b3a93e33764fb752f27bca3feda1312182517bbf7babd5f3700bb9b8de0ef6c35b1ae6e2ce7ab0b69

Source25: http://ftp.x.org/pub/individual/font/font-misc-cyrillic-1.0.3.tar.bz2
%define sha512 font-misc-cyrillic-1.0.3.tar.bz2=75e49cdb633f7ce5b9612d5adb0a85471c8fde5d55e8ccd9302f79f01e99e78b02449642c2cf785289f58d833bfa62042fce4253093fb17c87471559d1f9bdbf

Source26: http://ftp.x.org/pub/individual/font/font-misc-ethiopic-1.0.4.tar.bz2
%define sha512 font-misc-ethiopic-1.0.4.tar.bz2=4fed9ff3782746898c56dac199e9ca89356f4967779937049b9ff4ffad202317c023859f92d44b371dfa5485d5368ccad648e64b12cde0ed21f7d4aee5affcd5

Source27: http://ftp.x.org/pub/individual/font/font-misc-meltho-1.0.3.tar.bz2
%define sha512 font-misc-meltho-1.0.3.tar.bz2=3f42fe3e127f74259d50754f4bb6d2560cb32d810fecf663bd09fddb34829d29b48f3cbfaf43d02dab70b559afb2f806f321076f83450ff3871604345a0cdb56

Source28: http://ftp.x.org/pub/individual/font/font-misc-misc-1.1.2.tar.bz2
%define sha512 font-misc-misc-1.1.2.tar.bz2=d0bf74142f9621746846ea7a6fe9ae298a303a09c65e05c7decb4f37b2f513a88d727bf3dc5a3566c30de83b83493f164be0118b41d704464f75700b55018c74

Source29: http://ftp.x.org/pub/individual/font/font-mutt-misc-1.0.3.tar.bz2
%define sha512 font-mutt-misc-1.0.3.tar.bz2=7b152f6c1464d806b1f76664d9b619858c3cb3ea63027b6be1f69897e939e3a0b5312ddf230e0a42a8f3e3701e50f41917cac6ce566c05bc74dfa49bdf2ed4db

Source30: http://ftp.x.org/pub/individual/font/font-schumacher-misc-1.1.2.tar.bz2
%define sha512 font-schumacher-misc-1.1.2.tar.bz2=f37a2bfce95458b11376c89767b5adaea03dcecd7ed5b99a19a3d263f48e70b15bf679826a794c55da26b5f1635ea5fa5772ffe44c9f77a1daab0744ed92300a

Source31: http://ftp.x.org/pub/individual/font/font-screen-cyrillic-1.0.4.tar.bz2
%define sha512 font-screen-cyrillic-1.0.4.tar.bz2=58f12a4cbd18e323daad75b32a01ab3980dca0046f8dd94ff4452606ab9316b8a208dda3bc8e9346c02993bd2b8bb2b3dfe3413ccf9fc6a907fc1ea5d236fa51

Source32: http://ftp.x.org/pub/individual/font/font-sony-misc-1.0.3.tar.bz2
%define sha512 font-sony-misc-1.0.3.tar.bz2=c397b4e5081b2946799d701b8c48fca9fd2d55b8fa1dd96d2b29c5cd9996bb7356ae12671bf3bd964e6313bdc154020ed6377534e59ce53067e955e4b37aee1d

Source33: http://ftp.x.org/pub/individual/font/font-sun-misc-1.0.3.tar.bz2
%define sha512 font-sun-misc-1.0.3.tar.bz2=52c4a38e49a94831999652d9830da841949c319083ea40492e83690e1e5c2d31ea1979046a420af0e51bc105b8697bb06b4a438485e82b130d7469ad4519e275

Source34: http://ftp.x.org/pub/individual/font/font-winitzki-cyrillic-1.0.3.tar.bz2
%define sha512 font-winitzki-cyrillic-1.0.3.tar.bz2=f98fa99c1b0e60160b362310a7fe5fd5798aaa686751a6784a697c546ed754e885537eeed39a1f973dbceabc962cb65b39af1d336649381a49feb6df9f23e2b7

Source35: http://ftp.x.org/pub/individual/font/font-xfree86-type1-1.0.4.tar.bz2
%define sha512 font-xfree86-type1-1.0.4.tar.bz2=2b4afc6cbb7953f8ba4aab7862d16b7b988ea6a4df6de8d41c8340d35a1cd53d6fcc26479ff88189d1de9f42804e4f56d70e9dbd7e75820eab4ac6ae3a96840c

Source36: license.txt
%include %{SOURCE36}

BuildRequires:     pkg-config
BuildRequires:     xorg-applications
BuildRequires:     util-macros
BuildRequires:     libXfont2-devel
BuildRequires:     font-util-devel

Requires:          font-util

%description
The Xorg font packages provide needed fonts to the Xorg applications.

%prep
# Using autosetup is not feasible
%setup -q -c %{name}-%{version} -a0 -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a26 -a27 -a28 -a29 -a30 -a31 -a32 -a33 -a34 -a35

%build
for pkg in `ls` ; do
    pushd $pkg
    %configure
    make %{?_smp_mflags}
    popd
done

%install
for pkg in `ls` ; do
    pushd $pkg
    make DESTDIR=%{buildroot} install
    popd
done
install -vdm 755 %{buildroot}%{_datadir}/fonts
ln -svfn %{_prefix}/share/fonts/X11/OTF %{buildroot}%{_datadir}/fonts/X11-OTF
ln -svfn %{_prefix}/share/fonts/X11/TTF %{buildroot}%{_datadir}/fonts/X11-TTF

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 7.7-4
- Release bump for SRP compliance
* Wed Jan 11 2023 Shivani Agarwal <shivania2@vmware.com> 7.7-3
- Upgrade encodings, font-alias, font-misc-ethiopic
* Sat Dec 3 2022 Shivani Agarwal <shivania2@vmware.com> 7.7-2
- Removed font-util source
* Wed May 20 2015 Alexey Makhalov <amakhalov@vmware.com> 7.7-1
- initial version
