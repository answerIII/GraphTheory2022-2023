all: compil clean start

compil: main.o
	g++ -std=c++20 main.o -o a.out -larmadillo

main.o:
	g++ -std=c++20 -c main.cpp 

start:
	./a.out

clean:
	rm *.o
