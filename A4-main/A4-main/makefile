CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: a2

clean:
	rm -f *.o *.so molecule.py

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -lpython3.7m -lmol -dynamiclib -L. -L "/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu" -o _molecule.so

swig: molecule.i
	swig3.0 -python molecule.i

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -I "/usr/include/python3.7m" -o molecule_wrap.o

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

a2: swig libmol.so _molecule.so
