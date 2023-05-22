all: compil clean start

compil: main.o
	g++ main.o -o a.out

main.o:
	g++ -c main.cpp

start:
	./a.out

clean:
	rm *.o
