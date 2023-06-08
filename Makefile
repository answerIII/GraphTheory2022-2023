all: compil start

compil: 
	g++ -std=c++20 main.cpp -o a.out -larmadillo 

start:
	./a.out

clean:
	rm *.o
