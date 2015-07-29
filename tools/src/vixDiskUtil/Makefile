INCLUDEDIR=/usr/include
LIBDIR=/usr/lib/vmware

all: vix-disklib-util

clean:
	$(RM) ../../bin/vixdiskutil

vix-disklib-util: vixDiskUtil.cpp
	$(CXX) -o ../../bin/vixdiskutil -I$(INCLUDEDIR) -L$(LIBDIR) $? -ldl -lvixDiskLib -lvixMntapi -lvixDiskLibVim -lpthread -lssl -lfuse
