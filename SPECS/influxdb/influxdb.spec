Name:           influxdb
Version:        1.6.0
Release:        23%{?dist}
Summary:        InfluxDB is an open source time series database
License:        MIT
URL:            https://influxdata.com
Source0:        https://github.com/influxdata/influxdb/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=bbeddde2ff5498cb7ca3339d6edcac62b8be3b32550eab315d99d47621787390903fbd1d1cb7c8e9b66fa5836e01b4d052dacc70e1782939d3a67ab0a08be4a5
Source1:        influxdata.tar.gz
%define sha512  influxdata=61d7427da9b4e05965bcaf74e856747168424e0dbc8aa892406705dc80ad0dda6a1ff9682d36cd6136cbaa1873d852ac086411b94036c34d0d73090eb56fbfde
Source2:        liner.tar.gz
%define sha512  liner=96c3af7c4ecc252eb59389745c16174833e484d2cd3323707bb78db4c7a0c479ca3daea68f9ef75ff78ca98583f09a4e97525e812d7c7e165ddc885aae91125a
Source3:        toml.tar.gz
%define sha512  toml=f0a9e5bdb0ba5fa82ca2a25d77c521a55aec53f39e065ae7d01b8a0e089c078c8209fd2c32599d07d85e96982491b67492905cb12c149d09978c022c02f5f1f3
Source4:        roaring.tar.gz
%define sha512  roaring=c5cdd26a8d8431440132deebe10f8516cad03bd8a16b6fcb337c9bc52a2936e2b94c7c271d2a4bbf474a28c5494e5f7258d529b5c704876eccc501d8049a01c4
Source5:        pat.tar.gz
%define sha512  pat=cf758f046e42137302dc65f54034e33a5c9294bacb5a155d3b483b848bbf3c0274f3b7543fba3bf68766396e54804347f307bf383c4d9c03501e194e50700916
Source6:        xxhash.tar.gz
%define sha512  xxhash=8e3b3b8d6a7eb9e15e341aa6e788ae4526f58d5e2d8e2f7bdb086fb300035c79aacd9e63340c4f87258d6ebc9f53469909bea31097ca737b382f7286dbf34716
Source7:        jwt-go.tar.gz
%define sha512  jwt-go=25cff1e360c49dc1fe8d932690e20392e82394b5f0357990af1541c1c480fc698784062c7996b6ca59a2b822398ba9dd0214abde45ca4776b2cf489d01c2e4fe
Source8:        go-bitstream.tar.gz
%define sha512  go-bitstream=ae00d987f39b7140236afc96ab908a7f6ed5930dcfa081f1ef892931d773bce3a573e8ae9f8416c4d47697e354bd1de317a3d5716b6da7575f8d7162486f920c
Source9:        snappy.tar.gz
%define sha512  snappy=fe282fb77a2118a29e1cd7d76b7546f66c27d8fcd81ffe0aed9175e9533a184cb8af21ede4ad5e7af6eafc640fb1fef021ee801152c65c380cff08b1430f5051
Source10:       zap-logfmt.tar.gz
%define sha512  zap-logfmt=cc768b838f4c051bcb4e4b76bbde2d35e05b97a0522bac97f350e204597bd2334844f5e0ff9e0db8f034c994270afcd2c65818468ce6ffd31a739b14105f3fdf
Source11:       encoding.tar.gz
%define sha512  encoding=b5b2e75991b5ca25738b7db09b422416718fba8247bfda7dcb9412a508efe6e6fb07d420de50effa7d76ca38b6cec34f7d3181948fc35e62ede22656bebdc74e
Source12:       go-isatty.tar.gz
%define sha512  go-isatty=b89667a7800a5f7ad250ab3c1b6cdcf892b7671b4cf68c9d63916ab05f663263159c6d39254555a5730faf63813577f97a140db365bfa51a876499aedadeea4b
Source13:       opentracing-go.tar.gz
%define sha512  opentracing-go=2880ae28dcfb8a1261949569786fb3d41d351c99987c3185ff074c40cf2d49fd379450f00bf7e99c38ffe00049f12c40019aa4236cfbb2b2626d9d7499a8b342
Source14:       client_golang.tar.gz
%define sha512  client_golang=fbd9bb54048e97908cc7303d557ad78990eaede172b7423b84b9bc66218ba832d6cb69dc8b4535c97710ed2710c9af944b01bbf72bff02eaa8dc88a5cdcfd1b2
Source15:       msgp.tar.gz
%define sha512  msgp=629b9c442cab0f4bce993c79058479c751d2b05fa43947ba97756632830efd9747c46bf030e565c9332802e50dbe0f5d195d778f07e16306f5b343d588819501
Source16:       treeprint.tar.gz
%define sha512  treeprint=230d4d0754e16efcd70f464c08f214934a9e315b512f6bebd01b73df561c66a1ea2be96a9bb7d87be5b771a0f3b8e057bed5d770448747e9ad842e9a6283fe2e
Source17:       hllpp.tar.gz
%define sha512  hllpp=2b12deb156d171622a58dd9ba56aedbd0e4e33d2a667f078ab52548494c226003dd094acdef7cbba1c39e6ef9ff3080fcd8940902984c045216d20bd59d2ae5e
Source18:       bolt.tar.gz
%define sha512  bolt=ea3356ab86ddcbb7639bdc6fa6b8aedb4de9149b5f5f41ef2b20c6dd68909d8c436d39165b2aed244d0532b20a3111bd74e5fa6ed43a9fbd88a3c899dab3515c
Source19:       pgzip.tar.gz
%define sha512  pgzip=25c4013707975641983da0af7f32dbf1a241a45f9586d513dd512adf621afb4d9209c2b2fbbf406bd087404a475cacd73af2cfee72b8e0c1128dc63aef418c0b
Source20:       ratecounter.tar.gz
%define sha512  ratecounter=a08b0bf1cf20bd448d422a2c7445cc1893d1f10cd82da4baded0739f4178c5716eca8a8afa235aaaef6cfa9093efe5b7c5222033cc466c630d1f282de47a51f8
Source21:       x-golang.tar.gz
%define sha512  x-golang=43d29e53f66eaebf712f31590336894f91494f0b7343a39905c14868ad3ccb9b2ecddca54ea6381d6d62c97a794d30744b3ba1437d68d7d36eb46d6ede434d1d
Source22:       collectd.org.tar.gz
%define sha512  collectd.org=faa3d2785cc07bac04db8e1753404b0c9c1f85d422323398d6d52200453cc5a8ca8e60910a16455b4ade108dbee4a8213e3724a9a2937da74bf1e4211760e5a9
Source23:       protobuf-gogo.tar.gz
%define sha512  protobuf-gogo=556c88db396e780ef1bca1c83c589fff663c87958b2152d05c358821f6f54f970c48dbb88401464fd759dbb02e2498a6c02e185b90e3d3511fdd2e11ee95d9b2
Source24:       go-runewidth.tar.gz
%define sha512  go-runewidth=4e9fefa98db8498438b71b600723c0a73d6ce27351e4da2c7c0ef0df1ef2cfc0b1e53f24f906f21a6e532643959b9b9d6503a8d27b78c12207456537d08470c7
Source25:       perks.tar.gz
%define sha512  perks=fc864e7e9f03a4090b556c21b9a734333ca3962fcd0f4dfa64b07dabbbf80d05220e4a6bb8bf5da52ccc37bac73956f04b5d58f7042f97db2a3f1fb841086274
Source26:       go-unsnap-stream.tar.gz
%define sha512  go-unsnap-stream=d5272e18a57d631ec76161762f93d5258ba2b919a9dc6b706b64f5d70090616049d4b762f3d80d062afe58aebf4cb346b7500413d1828bf6111c6accbb9acf35
Source27:       protobuf-golang.tar.gz
%define sha512  protobuf-golang=1b1e0ae763e5e465529c3a6c98df821aa622862f5ab68a189b26fa8c48555e130c352235b63753f582f02d3121e50f755a493f19b7ff2d4ce5d4e42a97521b9e
Source28:       fwd.tar.gz
%define sha512  fwd=0da2880a25f8476bd43f9d63e1ac69530ae667ac862785606897be2df91045d0a105d063d637fc432753f7a8e57cf6af340de3574cb0536716537482f0cda98c
Source29:       client_model.tar.gz
%define sha512  client_model=9d2506e21cd7016362382346d02052fb72af9aaed92f924def5bec9bb5db3c41a1700ab29447411522915b47c076174400428c4ddc4fe37c5fea7e270f69f834
Source30:       common-prometheus.tar.gz
%define sha512  common-prometheus=67656ca7a4dc5a3980f54ab5091fb36333068c01e21b476df8f3f34fd588c567c7496f0e34e67af9615933ea1d701d4067e254e08c7fbec1437e0968a2950ebe
Source31:       procfs-prometheus.tar.gz
%define sha512  procfs-prometheus=eb85a3574a72bd1ca3f4e8a53135fdc25f4ad7eadcd909fe0a91926bca2a27cce579a40c01dd16843cc416aedb3c4f1cdc6913c51f4ef2a8dc3b7480c9e7e793
Source32:       zap-gouber.tar.gz
%define sha512  zap-gouber=e83653882ebb9c9a781e9e6e08c9955eaf482ac4070086c1f3f098be1c5f66b13a295419e9676597eeea588ecfd305c010ed2f92e232052ac4468000fda3357e
Source33:       compress.tar.gz
%define sha512  compress=eadaff172a788476b9f7f23409c308a6ea9022bbba8667b912247820d7fa8de9f8e348c46f89bb45e3fe7831b159fb5facfb44a3872ffb7d4ae5e32247b82a02
Source34:       crc32.tar.gz
%define sha512  crc32=8fa463cee64e8ee9ae8e48c690fc270c24cc1218471309632e6442015609891f9e03bb3a395ce09571c54fbb9f820844565d755eef389e0852a6d77a08604517
Source35:       golang_protobuf_extensions.tar.gz
%define sha512  golang_protobuf_extensions=f3de9ee65225f5bc418e015e354bf112c2cd9f65f28c36744cd05377b3444b7acd9560ccefd5a1ec1e3609fd3b161d128c5dba9ecb727ec6f2db6d826ef843f2
Source36:       atomic.tar.gz
%define sha512  atomic=0cc667693beb368436ce4cecb03ef16cc557700acc442515f94624c3c3e2bc27b45271e2a14ca6310899edf794e9b8fd6b2e6d2e238510ed05862a662c75464d
Source37:       multierr.tar.gz
%define sha512  multierr=e495684980cc80c5633a0940fd84c80e26701982ebfaa887e1c9d99e3e7685dfd1d78fcfbd626f3b96456977434ccddbba3ed315050d39277d5b09228e9d1cd1
Source38:       cpuid.tar.gz
%define sha512  cpuid=457a87d0f8f72a6ff13d55dd817e26aacf0d44cff8c29384d93a1f6d24f23d9fbf2a3ca151683f402a7bd2ab0849979077a2aeda121f504e4ac65e2dbd6165f3
Source39:       yamux.tar.gz
%define sha512  yamux=89819a60f8c4b5e84fefd5a4e013c994fb621ebe8dc4200ebf9666a32da819147eb24c9a6442b6015200f99ffa579eb85497e56a69de1164d01b3092ccc71ddf

Patch0: CVE-2019-20933.patch

Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Applications/Database
BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd
Requires:       systemd
Requires:       shadow

%description
InfluxDB is an open source time series database with no external dependencies.
It's useful for recording metrics, events, and performing analytics.

%prep
%autosetup -N -c -T -a 0 -n build/src/github.com/influxdata
%autosetup -N -D -c -T -a 1 -n build/src/github.com/influxdata
%autosetup -N -D -c -T -a 2 -n build/src/github.com/peterh
%autosetup -N -D -c -T -a 3 -n build/src/github.com/BurntSushi
%autosetup -N -D -c -T -a 4 -n build/src/github.com/RoaringBitmap
%autosetup -N -D -c -T -a 5 -n build/src/github.com/bmizerany
%autosetup -N -D -c -T -a 6 -n build/src/github.com/cespare
%autosetup -N -D -c -T -a 7 -n build/src/github.com/dgrijalva
%autosetup -N -D -c -T -a 8 -n build/src/github.com/dgryski
%autosetup -N -D -c -T -a 9 -n build/src/github.com/golang
%autosetup -N -D -c -T -a 10 -n build/src/github.com/jsternberg
%autosetup -N -D -c -T -a 11 -n build/src/github.com/jwilder
%autosetup -N -D -c -T -a 12 -n build/src/github.com/mattn
%autosetup -N -D -c -T -a 13 -n build/src/github.com/opentracing
%autosetup -N -D -c -T -a 14 -n build/src/github.com/prometheus
%autosetup -N -D -c -T -a 15 -n build/src/github.com/tinylib
%autosetup -N -D -c -T -a 16 -n build/src/github.com/xlab
%autosetup -N -D -c -T -a 17 -n build/src/github.com/retailnext
%autosetup -N -D -c -T -a 18 -n build/src/github.com/boltdb
%autosetup -N -D -c -T -a 19 -n build/src/github.com/klauspost
%autosetup -N -D -c -T -a 20 -n build/src/github.com/paulbellamy
%autosetup -N -D -c -T -a 21 -n build/src/golang.org/
%autosetup -N -D -c -T -a 22 -n build/src/
%autosetup -N -D -c -T -a 23 -n build/src/github.com/gogo
%autosetup -N -D -c -T -a 24 -n build/src/github.com/mattn
%autosetup -N -D -c -T -a 25 -n build/src/github.com/beorn7
%autosetup -N -D -c -T -a 26 -n build/src/github.com/glycerine
%autosetup -N -D -c -T -a 27 -n build/src/github.com/golang
%autosetup -N -D -c -T -a 28 -n build/src/github.com/philhofer
%autosetup -N -D -c -T -a 29 -n build/src/github.com/prometheus
%autosetup -N -D -c -T -a 30 -n build/src/github.com/prometheus
%autosetup -N -D -c -T -a 31 -n build/src/github.com/prometheus
%autosetup -N -D -c -T -a 32 -n build/src/go.uber.org
%autosetup -N -D -c -T -a 33 -n build/src/github.com/klauspost
%autosetup -N -D -c -T -a 34 -n build/src/github.com/klauspost
%autosetup -N -D -c -T -a 35 -n build/src/github.com/matttproud
%autosetup -N -D -c -T -a 36 -n build/src/go.uber.org/
%autosetup -N -D -c -T -a 37 -n build/src/go.uber.org/
%autosetup -N -D -c -T -a 38 -n build/src/github.com/klauspost
%autosetup -N -D -c -T -a 39 -n build/src/github.com/influxdata

cd %{name}-%{version}
%patch0 -p1

%build
export GO111MODULE=auto
export GOPATH=%{_builddir}/build
mkdir -p %{_builddir}/bin
export GOBIN=%{_builddir}/build/bin
export PATH=$PATH:$GOBIN
cd %{_builddir}/build/src/github.com/influxdata
mv -f %{name}-%{version} %{name}
cd %{name}
go clean $PWD/...
go install $PWD/...

%check
go test -run=TestDatabase . -v

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/influxdb
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/influxdb
mkdir -p %{buildroot}%{_localstatedir}/log/influxdb
cp -r %{_builddir}/build/bin/* %{buildroot}%{_bindir}
cp %{name}/etc/config.sample.toml %{buildroot}%{_sysconfdir}/influxdb/influxdb.conf
cp %{name}/scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/influxdb
cp %{name}/scripts/influxdb.service %{buildroot}%{_prefix}/lib/systemd/system
cp %{name}/man/influx.txt %{buildroot}%{_mandir}/man1/influx.1
cp %{name}/man/influx_inspect.txt %{buildroot}%{_mandir}/man1/influx_inspect.1
cp %{name}/man/influx_stress.txt %{buildroot}%{_mandir}/man1/influx_stress.1
cp %{name}/man/influx_tsm.txt %{buildroot}%{_mandir}/man1/influx_tsm.1
cp %{name}/man/influxd-backup.txt %{buildroot}%{_mandir}/man1/influxd-backup.1
cp %{name}/man/influxd-config.txt %{buildroot}%{_mandir}/man1/influxd-config.1
cp %{name}/man/influxd-restore.txt %{buildroot}%{_mandir}/man1/influxd-restore.1
cp %{name}/man/influxd-run.txt %{buildroot}%{_mandir}/man1/influxd-run.1
cp %{name}/man/influxd-version.txt %{buildroot}%{_mandir}/man1/influxd-version.1
cp %{name}/man/influxd.txt %{buildroot}%{_mandir}/man1/influxd.1

%clean
rm -rf %{buildroot}/*

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group %{name} >/dev/null || groupadd -r %{name}
    getent passwd %{name} >/dev/null || useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
            -c "InfluxDB" %{name}
fi

%post
chown -R %{name}:%{name} /var/lib/%{name}
chown -R %{name}:%{name} /var/log/%{name}
%systemd_post influxdb.service

%preun
%systemd_preun influxdb.service

%postun
%systemd_postun_with_restart influxdb.service
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel %{name}
    groupdel %{name}
fi

%files
%defattr(-,root,root,755)
%dir %config(noreplace) %{_sysconfdir}/influxdb
%dir %{_sharedstatedir}/influxdb
%dir %{_localstatedir}/log/influxdb
%config(noreplace) %{_sysconfdir}/influxdb/influxdb.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/influxdb
%{_prefix}/lib/systemd/system/influxdb.service
%{_bindir}/influxd
%{_bindir}/influx
%{_bindir}/influx_inspect
%{_bindir}/influx_stress
%{_bindir}/influx-tools
%{_bindir}/influx_tsm
%{_mandir}/man1/*
%exclude %{_bindir}/store
%exclude %{_bindir}/stress_test_server
%exclude %{_bindir}/test_client

%changelog
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-23
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-22
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-21
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-20
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-19
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.6.0-18
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-17
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-16
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.6.0-15
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.6.0-14
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.6.0-13
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.6.0-12
- Bump up version to compile with new go
* Fri Dec 04 2020 HarinadhD <hdommaraju@vmware.com> 1.6.0-11
- Bump up version to compile with new go
* Thu Dec 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-10
- Fix for CVE-2019-20933
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.6.0-9
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.6.0-8
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-7
- Bump up version to compile with go 1.13.3
* Fri Oct 11 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-6
- Build with go 1.13
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.6.0-5
- Bump up version to compile with new go
* Fri Jan 25 2019 Keerthana K <keerthanak@vmware.com> 1.6.0-4
- Added make check.
* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 1.6.0-3
- Build using go 1.9.7
* Thu Oct 25 2018 Ajay Kaher <akaher@vmware.com> 1.6.0-2
- Fix for aarch64
* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 1.6.0-1
- Initial influxdb package for Photon.
