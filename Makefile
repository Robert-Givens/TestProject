all: myprogram

myprogram: myprogram.o
    gcc -o myprogram myprogram.o

myprogram.o: myprogram.c
    gcc -c myprogram.c

clean:
    rm -f myprogram.o myprogram
