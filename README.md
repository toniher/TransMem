TransMem
========

Tool for assigning putative transmembrane regions in a protein sequence

Reference:
'TransMem': a neural network implemented in Excel spreadsheets for predicting transmembrane domains of proteins.
http://www.ncbi.nlm.nih.gov/pubmed/9183525

Build
=====

Within the same directory simply execute: make

transmem executable will be created.


Usage 
=====

	transmem -w 12 -d Q9BTV4.fasta
	
This reads Q9BTV4.fasta file with a 12 window size and debugging option.


Output
======

Lines starting with '#' are debug output and offers information about every residue.

Result lines include separated by tabs:

* IDs of FASTA entries
* a candidate transmembrane stretch of aas
* starting and ending positions within the query sequence.


#sp|Q9BTV4|TMM43_HUMAN@392|R->-1.1
#sp|Q9BTV4|TMM43_HUMAN@393|V->-1.1
#sp|Q9BTV4|TMM43_HUMAN@394|P->-1.1
#sp|Q9BTV4|TMM43_HUMAN@395|A->-1.1
#sp|Q9BTV4|TMM43_HUMAN@396|K->-1.1
#sp|Q9BTV4|TMM43_HUMAN@397|K->-1.1
#sp|Q9BTV4|TMM43_HUMAN@398|L->-1.1
#sp|Q9BTV4|TMM43_HUMAN@399|E->-1.1
sp|Q9BTV4|TMM43_HUMAN	GMFVGLMAFLLSFYL	34	49
sp|Q9BTV4|TMM43_HUMAN	AAGWMAMFMGLNLM	312	326
sp|Q9BTV4|TMM43_HUMAN	LVNIGLKAFAFCVATSLTLLTVAAGWLF	342	370
sp|Q9BTV4|TMM43_HUMAN	LWALLIAGLALVPIL	373	388

