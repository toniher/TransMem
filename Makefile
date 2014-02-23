all:transmem.cpp SNNS.gbl kseq.h
	$(CXX) -g -O2 transmem.cpp -o transmem -lz

clean:
	rm -f *.o transmem

