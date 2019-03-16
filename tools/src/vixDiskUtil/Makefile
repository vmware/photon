INCLUDEDIR=/usr/lib/vmware-vix-disklib/include
LIBDIR=/usr/lib/vmware-vix-disklib/lib64

all: vix-disklib-util

clean:
	$(RM) ../../bin/vixdiskutil

vix-disklib-util: vixDiskUtil.cpp
	$(CXX) -o ../../bin/vixdiskutil -I$(INCLUDEDIR) -L$(LIBDIR) $? -ldl -lvixDiskLib -lvixMntapi -lvixDiskLibVim -lpthread -lssl -lfuse
