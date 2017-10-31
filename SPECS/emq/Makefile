
FINAL_OUTPUT_DIR=FINAL_RPMS
TARBALL_DIR=dist
TOP_DIR=$(shell pwd)
DEFINES=--define '_topdir $(shell pwd)' --define '_tmppath $(shell pwd)/tmp' --define '_sysconfdir /etc' --define '_localstatedir /var'
rpms:	clean package

prepare:
	mkdir -p BUILD SOURCES SPECS SRPMS RPMS tmp dist emqttd-${EMQ_VERSION}
	git clone -b emq22 https://github.com/emqtt/emq-relx.git emqttd-${EMQ_VERSION}
	cd emqttd-${EMQ_VERSION} && make
	rm -rf emqx-${EMQX_VERSION}/deps/gen_rpc/_build/
	tar -zcf emqttd-${EMQ_VERSION}.tar.gz emqttd-${EMQ_VERSION}
	cp -R emqttd-${EMQ_VERSION} dist
	cp emqttd-${EMQ_VERSION}.tar.gz SOURCES
	cp emqttd.spec SPECS

package: prepare
	mkdir -p $(FINAL_OUTPUT_DIR)
	rpmbuild -vv -bb --nodeps SPECS/emqttd.spec $(DEFINES)
	mkdir ../package
	cp -r RPMS/x86_64/emqttd-${EMQ_VERSION}* ../package
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqttd-${EMQ_VERSION} emqttd-${EMQ_VERSION}.tar.gz

clean:
	rm -rf BUILDROOT BUILD SOURCES SPECS SRPMS RPMS tmp $(FINAL_OUTPUT_DIR) dist emqttd-${EMQ_VERSION} emqttd-${EMQ_VERSION}.tar.gz ../package
