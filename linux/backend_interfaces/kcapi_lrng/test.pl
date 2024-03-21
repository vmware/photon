#!/usr/bin/env perl
#
# Written by: Stephan Müller <smueller@chronox.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software", to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions: 
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
#		            NO WARRANTY
#
#    BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
#    FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
#    OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
#    PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
#    OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
#    TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
#    PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
#    REPAIR OR CORRECTION.
#
#    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
#    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
#    REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
#    INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
#    OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
#    TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
#    YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
#    PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGES.
#
#

use strict;
use warnings;
use IPC::Open2;
use Getopt::Std;
use MIME::Base64;

# Contains the command line options
my %opt;

#
# convert ASCII hex to binary input
# $1 ASCII hex
# return binary representation
sub hex2bin($) {
	my $in = shift;
	my $len = length($in);
	$len = 0 if ($in eq "00");
	return pack("H$len", "$in");
}

sub hex2bin_ccm($) {
	my $in = shift;
	my $len = length($in);
	return pack("H$len", "$in");
}

#
# convert binary input to ASCII hex
# $1 binary value
# return ASCII hex representation
sub bin2hex($) {
	my $in = shift;
	my $len = length($in)*2;
	return unpack("H$len", "$in");
}

my $DIR="/sys/kernel/debug/kcapi_lrng/";
sub writedata($$) {
	my $file=shift;
	my $data=shift;
	my $bytes=length($data);
	$file = $DIR . $file;
	open(FH, ">$file") or die "Cannot open file $file";
	syswrite(FH, $data, $bytes);
	close(FH);
}

sub readdata($$) {
	my $file=shift;
	my $bytes=shift;
	my $out = "";
	$file = $DIR . $file;
	open(FH, "<$file") or die "Cannot open file $file";
	my $len = sysread(FH, $out, $bytes);
	if(!defined($len)) {
		$out="";
	}
	return $out;
}

sub match($$$) {
	my $string=shift;
	my $exp=shift;
	my $act=shift;
	if($exp eq $act) {
		print "$string passed\n";
	} else {
		print "$string failed\nexp $exp\nact $act\n";
	}
}

my %SHA = (
	"SHA-1" => {
		name => "sha1",
		type => "0x00000002",
		msg => "8c899bba",
		exp => "ac6d8c4851beacf61c175aed0699053d8f632df8",
	},
	"SHA-256" => {
		name => "sha256",
		type => "0x00000002",
		msg => "6a3787",
		exp => "eaa566834797ac4f9313bd40c614e3cd40ded480bf08857d707da1639d0f3b14",
	},
	"SHA-384" => {
		name => "sha384",
		type => "0x00000002",
		msg => "fc7cb451",
		exp => "0f8832f9e468d41f94e7ecde129f0438a8b1628084a1d9e201a3f5d0963fbbbaf1df518b193cba6eb3b90306aa1895f6",
	},
	"SHA-512" => {
		name => "sha512",
		type => "0x00000002",
		msg => "3fd989f37133e8c9578a0740b5",
		exp => "3e9a1ddacd38ff9a302f1f86225db9fe38f279c8bb86e76190dcebec6b52060f7ad3485e8e598f433428845c1eb76ce645ab743e62bba8e4f69c40eaa9601741",
	},
	"SHA-512-2" => {
		name => "sha512",
		type => "0x00000002",
		msg => "00",
		exp => "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
	},
	"SHA-512-3" => {
		name => "sha512",
		type => "0x00000002",
		msg => "1e71b3ef200f2dc129b43cdb4d372aebcfdbfe6e8924fd238ee972bf0fa9abe27b23444aea20a847bc94d46e7de55e920c8bb6f0fdd9adaa3b1a3377f2e06598ac99c70eba63cd0ad522a1a505cf20d1c213258f59140b63928f6d059027305af8fcc4a25680a6f3bc862ae6ac9c7790379bd3b4677c2136db6da7d3b1241510a974c370861e3beab8e9f79a39f56cb7b54c47c5edbaf60c5ddf6a481c821ba205284ddf14e592d81273912a7581052e824d092cb47592cb610b3dcc9be74bf85541e957c67fb5a3134b7ffc28e94cdde6c7a14f8456fe5d2f19a8c7f4fcabfbe0e620406691ac35009a497a19d449ad2be29898250541a80f3233a1f0684691f0407903bac67d742487780b12eb038497c5746e5e296396497e67c357d321a3cb777c068bc3324ac63b9316d9d6824c7499c038f86a6d0e2424cb93f1e7461abab2b1b2a033d39e2ddd2205383cceeb08850160bc7266f7e94ce87a8649bcdc0519a16fc3bc6657a296ad3ff4c5f04b9cb2c14d6fe6563be12044e1dda48bd3f4d5d3a6ba06f55f6d8ebd2cd81aef5277488767dc7145c151c5692ebf9ebce5cf0ecfbd4eba879dd6ecd934abe3d3eae36edc16cab93c718466dfcbf4df55fcddeb1e1e478025f925d98abf34c7a4fa264c47c200664233c1292c1e441061ff6795472f6dffd65ba17c57353c6f6b69890b50d3472160ef4f36da9177d9e5d6b534d25a88e0a2ab93fec8fe8b83302154d37fb167929d8d77b6718a54e1eb690fef48065fca91d143866582e9aaf909cfcb5dc4286001f581d17773a4d17aa0bdee309abb66acb6f93db72a1e8cd009421c717552339410b5ae76b32f509b63065a1280645cfa40fd4a455cf1d2bc09f4ed432aacb55fc45a76f5b2bd07559a345b761f2253835896d697812c24c6f12e675c4cff8c69faba507dd8169eb02d8d18e5dfbdf450e70e0936029529f4a938b243441360ba9b1b65958d01bcb4045abae728fce668d3ab0aa945f58a501a5af58079b0da5b8dc6ddc53948096a07e2680262a8d1d406b60278b413efe22adc599c529ea153ba03df9544b12fd91f6f4bc0f5895f9a6676182cb6b9feb1c205051e39a45eaa081a938e1605d30932478ba84a6736c4dd35754cb2ad62c5cb1e218e958c",
		exp => "4c46d3d0527db2c5d66eeca506fffed6541e8cf7b082346d2eb0142f7461e9e5a162265315c7246e08f07a621a3d37a7c63f9c400fb77ff9a8c2fa1cc6191615",
	}
);

my %SYM = (
        "AES128-CBC" => {
		name => "cbc(aes)",
		type => "0x02000000",
		msg => "4e0c74c8d67862a9732604f62f4ad316",
		key => "790afba9cfbc095b682666a6999a38ed",
		iv => "fb1f88c0f23d6aa6dde475c018d7f482",
		exp => "7f7454245af4e67cd2296341f21dcba9",
        },
        "AES192-CBC-GFSbox" => {
		name => "cbc(aes)",
		type => "0x02000000",
		msg => "1b077a6af4b7f98229de786d7516b639",
		key => "000000000000000000000000000000000000000000000000",
		iv => "00000000000000000000000000000000",
		exp => "275cfc0413d8ccb70513c3859b1d0f72",
        },
	"AES-ECB" => {
		name => "ecb(aes)",
		type => "0x02000000",
		msg => "5ec0fd4db8131af11948b3bd2bf062f6",
		key => "10617fe4a8f00fbdc2f0611229d6a798",
		exp => "2a64d2e5ca43c2ce0fe9da7a380c5c8d",
	}
);

my %DRBG_NOPR =
(
	"DRBG1" => {
		name => "drbg_nopr_sha256",
		entropy => "a65ad0f345db4e0effe875c3a2e71f42c7129d620ff5c119a9ef55f05185e0fb8581f9317517276e06e9607ddbcbcc2e",
		expected => "d3e160c35b99f340b2628264d1751060e0045da383ff57a57d73a673d2b8d80daaf6a6c35a91bb4579d73fd0c8fed111b0391306828adfed528f018121b3febdc343e797b87dbb63db1333ded9d1ece177cfa6b71fe8ab1da46624ed6415e51ccde2c7ca86e283990eeaeb91120415528b2295910281b02dd431f4c9f70427df",
		addtla => "",
		addtlb => "",
		pers => "",
	},
	"DRBG2" => {
		name => "drbg_nopr_sha256",
		entropy =>
			"73d3fba3945f2b5fb98ff69c8a9317ae19c34cc3d6caa32d16fc42d22dd56f56cc1d30ff9e063e09ce58e69a35b3a656",
		expected =>
			"717b93461a40aa35a4aac5e76d5b5b8aa0df397dae71585b3c7cb4f089fa4a8ca95c54c040dfbcce268134f8ba7d1ce8ad21e074cf4884301fa1d54f81422ff4db0b23f87327b81d42f84458d85b29270af86959b57844eb9ee0686f429ab05be04ecb6aaae2d2d533253ee06cc76a07a503839fe28bd11c70a8075997ebf6be",
		addtla =>
			"f4d5983da8fcfa37b7546773c7c3dd473471025dc1a0d310c18bbdf566346fdd",
		addtlb =>
			"f79e6a560e73e9d97ad169e06f8c551c44d1ce6f28cca44da8c085d15a0c5940",
		pers => "",
	},
	"DRBG3" => {
		name => "drbg_nopr_sha256",
		entropy =>
			"2a85a98bd0da83d6adab9fbb543115951c4d499f6a15f6e415508806290ded8db96f96e1839ff788da84bf4428d91daa",
		expected =>
			"2d55dec9ed0547073d04fc280f92f04dd80032470a1b1c4befd997a11767da266cfe76466fbc6d824e838a98666c01b6e664e008106fd35d90e70d72a6a7e3bb9811125623c26dd1c8a87a39f334e3b8f86600777dcf3c3efac90fafe024fae984f96a01f635db5cab2aef4eacab55b89bef9868af51d816a55eaef91ed2dbe6",
		addtla => "",
		addtlb => "",
		pers =>
			"a880ec98309815d2c6c468f13a1cbfce6a4014eb369953da576bcea41c663dbc",
	},
	"DRBG4" => {
		name => "drbg_nopr_sha256",
		entropy =>
			"69ed82a9c57bbfe51d2fcb7ad3507d96b4b92b50775127743374baf130df8edf871d87bc96b2c3a7ed605e614e51291a",
		expected =>
			"a571243111fe13e1a82412fb37a127a5ab77a19fae8faf1393f7538591b61babd46beab6efda4c906eef5fdee1c71036d567bd14b689210cc9926564d0f323e07fd1e875c28506eacac0cb792d2982fcaa9ac6957edc8865baec0e1687eca39ed88c80ab3a64e0cb0e4598dd7c6c6c261113c8cea947a60657a266bb2d7ff3c1",
		addtla =>
			"74d36ddae8d6865f6301fdf27d06296d94d166f0d272674e77c53d9e03e3a578",
		addtlb =>
			"f6b63df07c2604c58bcd3e6a9f9c3a2edb4787e58e005e2b747fa6f680cd9b21",
		pers =>
			"74a6e008f927ee1d6e3c282087ddd7543147784be56da373a965b110c1dc777c",
	},
	"DRBG5" => {
		name => "drbg_nopr_hmac_sha256",
		entropy =>
			"ca851911349384bffe89de1cbdc46e6831e44d34a4fb935ee285dd14b71a7488659ba96c601dc69fc902940805ec0ca8",
		expected =>
			"e528e9abf2dece54d47c7e75e5fe302149f817ea9fb4bee6f4199697d04d5b89d54fbb978a15b5c443c9ec21036d2460b6f73ebad0dc2aba6e624abf07745bc107694bb7547bb0995f70de25d6b29e2d3011bb19d27676c07162c8b5ccde0668961df86803482cb37ed6d5c0bb8d50cf1f50d476aa0458bdaba806f48be9dcb8",
		addtla => "",
		addtlb => "",
		pers => "",
	},
	"DRBG6" => {
		name => "drbg_nopr_hmac_sha256",
		entropy =>
			"f97a3cfd91faa046b9e61b9493d436c4931f604b22f1081521b3419151e8ff0611f3a7d43595357d58120bd1e2dd8aed",
		expected =>
			"c6871cff0824fe55ea7689a52229886730450e5d362da5bf590dcf9acd67fed4cb32107df5d03969a66b1f6494fdf5d63d5b4d0d34ea7399a07d0116126d0d518c7c55ba46e12f62efc8fe28a51c9d428e6d371d7397ab319fc73ded4722e5b4f30004032a6128df5e7497ecf82ca7b0a50e867ef6728a4f509a8c859087039c",
		addtla =>
			"517289afe444a0fe5ed1a41dbbb5eb17150079bdd31e29cf2ff30034d8268e3b",
		addtlb => "88028d29ef80b4e6f0fe12f91d7449fe75062682e89c571440c0c9b52c42a6e0",
		pers => "",
	},
	"DRBG7" => {
		name => "drbg_nopr_hmac_sha256",
		entropy => "8df013b4d103523073917ddf6a869793059e9943fc8654549e7ab22f7c29f122da2625af2ddd4abcce3cf4fa4659d84e",
		expected => "b91cba4cc84fa25df8610b81b641402768a2097234932e37d590b1154cbd23f97452e310e291c45146147f0da2d81761fe90fba64f94419c0f662b28c1ed94da487bb7e73eec798fbcf981b791d1be4f177a8907aa3c401643a5b62b87b89d66b3a60e40d4a8e4e9d82af6d2700e6f535cdb51f75c321729103741030ccc3a56",
		addtla => "",
		addtlb => "",
		pers => "b571e66d7c338bc07b76ad3757bb2f9452bf7e07437ae8581ce7bc7c3ac651a9",
	},
	"DRBG8" => {
		name => "drbg_nopr_hmac_sha256",
		entropy => "c2a566a9a1817b15c5c3b778177ac87c24e797be0a845f11c2fe399dd37732f2cb1894eb2b97b3c56e628329516f86ec",
		expected => "b3a3698d777699a0dd9fa3f0a9fa57832d3cefac5df24437c6d73a0fe41040f1729038aef1e926352ea59de120bfb7b073183a34106efed6278ff8ad844ba0448115dfddf3319a82de6bb11d80bd871a9acd35c73645e1270fb9fe4fa88ec0e465409ea0cba809fe2f45e04943a2e396bbb7dd2f4e0795303524cc9cc5ea54a1",
		addtla => "413dd83fe56835abd478cb9693d67635901c40239a266462d3133b83e49c820b",
		addtlb => "d5c4a71f9d6d95a1bedf0bd2247c277d1f84a4e57a4a8825b82a2d097de63ef1",
		pers => "13ce4d8dd2db9796f94156c8e8f0769b0aa1c82c1323b61536603bca37c9ee29",
	},
	"DRBG9" => {
		name => "drbg_nopr_ctr_aes192",
		entropy => "c35c2fa2a89d52a11fa32aa96c95b8f1c9a8f9cb245a8b40f3a6e5a7fbd9d3c68e277ba9ac9bbb00",
		expected => "8c2e72abfd9bb8284db79e17a43a3146cd7694e35249fc3383914a7117f41368e6d4f148ff49bf29076b5015c59f457945662e3d3503843f4aa5a3df9a9df10d",
		addtla => "",
		addtlb => "",
		pers => "",
	},
	"DRBG10" => {
		name => "drbg_nopr_ctr_aes256",
		entropy =>
			"36401940fa8b1fba91a1661f211d78a0b9389a74e5bccfece8d766af1a6d3b14496f25b0f1301b4f501be30380a137eb",
		expected => "5862eb38bd558dd978a696e6df164782ddd887e7e9a6c9f3f1fbafb78941b535a64912dfd224c6dc7454e5250b3d97165e16260c2faf1cc7735cb75fb4f07e1d",
		addtla => "",
		addtlb => "",
		pers => "",
	},
	"DRBG11" => {
		name => "drbg_nopr_ctr_aes128",
		entropy =>
			"87e1c532997f57a35c286de864bff264a39e98db6c10787f",
		expected => "2c147e24119ad8d4b2ed61c153d050c924ff597515f1173a3df44b2c8428ef890eb9def3e47804b2fd9b357fe13f8a3e10c8670af9df2d6c96fbb2b8cb2dd6b0",
		addtla => "",
		addtlb => "",
		pers => "",
	},
	"DRBG12" => {
		name => "drbg_nopr_ctr_aes128",
		entropy =>
			"71bdce35427d20bf58cf1774ce72d83334502d8f5b14c4dd",
		expected => "9733e82012e27ba1468ff234b3c9b66b20b24fee27d80b218cff63736929fbf385cd888e432c718ba255d20f1d7fe3e12aa3e92c2589c714529956ccc3dfb381",
		addtla =>
			"66ef42d69a8c3d6d4a9e95a6914d8156",
		addtlb =>
			"e31883d94b5ec4ccaa612fbb4a55d1c6",
		pers => "",
	},
	"DRBG13" => {
		name => "drbg_nopr_ctr_aes128",
		entropy =>
			"ca4b1efa75bd69363873b8f9db4d350e47bf6c3772fdf7a9",
		expected => "59c319791bb1f30ee934ae6e8b1fad1f74ca254568b87f7512f8f2ab4c23010305e170ee75d8cbeb234c7a236e1227db6f7aac3c44b7874b6556744534300c3d",
		addtla => "",
		addtlb => "",
		pers =>
			"ebaa602c4dbe33ff1befbf0a0bc69754",
	},
	"DRBG14" => {
		name => "drbg_nopr_ctr_aes128",
		entropy =>
			"c0701f9250758fcdf2be739880db66eb1468b4a5879c2da6",
		expected => "97c0c0e5a0ccf24f3363488adb130a3589bf806562ee13957c33d37df407777a2b650b5f455c13f190777fc5043fcc1a38f8cd1bbbd557d14a4c2e8a2b491e5c",
		addtla =>
			"f901f8167a1dffde8e3c83e24485e7fe",
		addtlb =>
			"171c0938c2389f97876055b48216627f",
		pers =>
			"8008aee8e96940c50873c79f8ecfe002",
	},
);

sub hash() {
	foreach my $hash (sort keys %SHA) {
		my $out;
		writedata("name", $SHA{$hash}{name});
		writedata("type", $SHA{$hash}{type});
		if(defined($SHA{$hash}{key})) {
			writedata("key", hex2bin($SHA{$hash}{key}));
		}
		writedata("data", hex2bin($SHA{$hash}{msg}));
		$out = readdata("data", 10000);
		$out = bin2hex($out);
		$out = substr($out, 0, (length($SHA{$hash}{exp})));
		match("$hash:", $SHA{$hash}{exp}, $out);
	}
}

sub sym() {
	foreach my $sym (sort keys %SYM) {
		my $out;

		foreach my $blktype ("0x00000001", "0x00000100") {
			my $type = ($SYM{$sym}{type}) | $blktype;
			writedata("name", $SYM{$sym}{name});
			writedata("type", $type);
			writedata("key", hex2bin($SYM{$sym}{key}));
			if(defined($SYM{$sym}{iv})) {
				writedata("iv", hex2bin($SYM{$sym}{iv}));
			}
			writedata("data", hex2bin($SYM{$sym}{msg}));
			$out = readdata("data", 10000);
			$out = bin2hex($out);
			if ($blktype eq "0x00000100") {
				match("$sym blkcipher:", $SYM{$sym}{exp}, $out);
			} else {
				match("$sym ablkcipher:", $SYM{$sym}{exp}, $out);
			}
		}
	}
}

sub drbg($) {
	my $ref = shift;
	my %drbg_array = %$ref;
	foreach my $drbg (sort keys %drbg_array) {
		my $out;
		writedata("name", $drbg_array{$drbg}{name});
		writedata("type", "0x00000008");
		writedata("drbg_entropy", hex2bin($drbg_array{$drbg}{entropy}));
		if (defined($drbg_array{$drbg}{pers}) &&
		    $drbg_array{$drbg}{pers} ne "")
			{ writedata("drbg_pers", hex2bin($drbg_array{$drbg}{pers})); }
		if (defined($drbg_array{$drbg}{addtla}) &&
		    $drbg_array{$drbg}{addtla} ne "")
			{ writedata("drbg_addtla", hex2bin($drbg_array{$drbg}{addtla})); }
		if (defined($drbg_array{$drbg}{addtlb}) &&
		    $drbg_array{$drbg}{addtlb} ne "")
			{ writedata("drbg_addtlb", hex2bin($drbg_array{$drbg}{addtlb})); }
		if (defined($drbg_array{$drbg}{entpra}) &&
		    $drbg_array{$drbg}{entpra} ne "")
			{ writedata("drbg_entpra", hex2bin($drbg_array{$drbg}{entpra})); }
		if (defined($drbg_array{$drbg}{entprb}) &&
		    $drbg_array{$drbg}{entprb} ne "")
			{ writedata("drbg_entprb", hex2bin($drbg_array{$drbg}{entprb})); }
		$out = readdata("data", length($drbg_array{$drbg}{expected})/2);
		$out = bin2hex($out);
		match("$drbg:", $drbg_array{$drbg}{expected}, $out);
	}
}

hash;
sym;
drbg(\%DRBG_NOPR);
