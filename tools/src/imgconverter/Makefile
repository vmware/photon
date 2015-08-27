INLUDEDIR=/usr/include
LIBDIR=/usr/lib

all: img-converter

clean:
	$(RM) ../../bin/imgconverter

img-converter: imgConverter.c
	$(CXX) -o ../../bin/imgconverter -I$(INCLUDEDIR) -L$(LIBDIR) $? -ldl -lz -luuid
