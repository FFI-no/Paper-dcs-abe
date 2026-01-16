.PHONY: all clean

include ../../Makefile.common

# defined in Makefile.common
VERSION=${OPENSSL_VERSION}

all: package openssl-${VERSION}/.built
#all: openssl-${VERSION}/.built

DEST_LIBDIR := $(DEPS_INSTALL_ZROOT)/lib
DEST_INCLUDEDIR := $(DEPS_INSTALL_ZROOT)/include

# Need to replace __NR_eventfd with __NR_eventfd2 for it to compile on the
# Raspberry Pis (ARM), but this does not seem to be needed on x86_64.
openssl-${VERSION}/.built: openssl-${VERSION}
	cd $<; \
	grep -rl "=> qw/glob/" ./ | xargs sed --in-place 's/=> qw\/glob\//=> qw\/:glob\//g'; \
	grep -rl "__NR_eventfd" ./ | xargs sed -i 's/__NR_eventfd/__NR_eventfd2/g'; \
	./${OPENSSL_CONFIG} --prefix=$(DEPS_INSTALL_ZROOT) && \
	make && \
	make install_sw && \
	touch .built

package:
	./download_openssl.sh ${WITH_BP}

openssl-${VERSION}: openssl-${VERSION}.tar.gz
	tar -zxf $^

clean:
	rm -rf openssl-$(VERSION)

distclean:
	rm -rf openssl-$(VERSION)*
