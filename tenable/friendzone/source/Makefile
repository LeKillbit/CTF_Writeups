CC=g++

all:exe

object:
	$(CC) -c $(wildcard *.cpp)

exe: object
	$(CC) $(wildcard *.o) -o chall -g

clean:
	rm $(wildcard *.o)
