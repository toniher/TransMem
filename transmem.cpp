/*********************************************************
 TransMem C++ Core

 TransMembrane Prediction program based in ANN library

*********************************************************/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "SNNS.gbl"
#include "itoa.h"
#include <string>
#include <iostream>
#include <zlib.h>
#include "kseq.h"

#define Act_TanH_Xdiv2(sum, bias)(tanh((sum + bias)/2))

using namespace std;

KSEQ_INIT(gzFile, gzread)

float Argos21_3(const char *);


int main( int argc, char *argv[] ) {
	gzFile fp;
	kseq_t *seq;
	int l;
	
	if (argc == 1) {
		fprintf(stderr, "Usage: %s <fastafile>\n", argv[0]);
		return 1;
	}
	
	fp = gzopen(argv[1], "r");
	seq = kseq_init(fp);
	while ((l = kseq_read(seq)) >= 0) {
		printf("name: %s\n", seq->name.s);
		if (seq->comment.l) printf("comment: %s\n", seq->comment.s);
		printf("seq: %s\n", seq->seq.s);
		if (seq->qual.l) printf("qual: %s\n", seq->qual.s);
	}
	
	printf("return value: %d\n", l);
	kseq_destroy(seq);
	gzclose(fp);
	return 0;

	// Need to start function from here

	double beg;
	double fin;
	int ent; 
	char* ide;
	char* protseq;
	int check;


	string Neuras(string, string);


	double Beginning, Finish;

	int numf, dec, sig;
	string ID, NeuroText, stringi, stringf, sbloc, seloc, sres, Numstring, Resstring, Detstring, stringF, ssign;
	int Minimum, Checked;

	// Control variables

	Beginning=beg;	
	Finish=fin;
	Minimum=ent;	// Minimum TM stretch size

	Checked=check;	// Display correspondence to NN


	ID = ide;	// ID of peptide
	NeuroText= protseq;	// Sequence

	int i, LonSeq, Primero, Tamanyo;
	string Salida,Resultado;

	int Numero, bloc, eloc;
	float *NumRes;
	float Inic, Fina, Der, Izq, Max;
	int LastTM, CutOff;

	//Control variables are assigned
	Inic=Beginning;
	Fina=Finish;
	CutOff=Minimum;

	//Array of mappings to NN made from seq length
	LonSeq = NeuroText.length(); 
	NumRes = (float *)calloc(LonSeq+1,sizeof(float)); 

	Resultado = NeuroText;

	// cout << ID + "\n" + NeuroText+ "\n" <<LonSeq << " residues\n\n"; //Print out ID, sequence and num of residues.

	NeuroText="XXXXXXXXXX"+NeuroText+"XXXXXXXXXX";


	// Begin iteration for sequence

	for(i=1;i<LonSeq;i++){

		NumRes[i]=Argos21_3(NeuroText.substr((long int)i,21).c_str()); // Sent to Argos
	
		if(Checked==1){

			// Display NN mappings
			Numero = i;
		
			Numstring = (string)itoa(Numero);
			Resstring = (string)fcvt(NumRes[i], numf, &dec, &sig);
		
			if (sig==1) {ssign="-";}
			if (sig==0) {ssign="+";}
		
			Detstring = Numstring + "|" + NeuroText.substr((long int)(i+10),1)+"->" + ssign + (string)itoa(dec) + "." + Resstring + "&";
		
			//cout << Numero << " " + NeuroText.substr((long int)(i+10),1)+"-> "<< NumRes[i] <<"\n";
		
			stringF+=Detstring;


		
		}
	}

	i=1;
	LastTM=0;

	while(i<LonSeq){
		Tamanyo=1;
		Primero=i;
	
		if(Inic<=NumRes[i]){

		// If residue upper than threshold defined...

				while(true){
		
					if(Primero>(LastTM+1) || (Primero+Tamanyo)<LonSeq){

						if(Primero>(LastTM+1)) {Izq=NumRes[Primero-1];}

						else {Izq=-1;}

						if((Primero+Tamanyo)<LonSeq) {Der=NumRes[Primero+Tamanyo+1];}

						else {Der=-1;}

						Max=(Der>Izq)?Der:Izq;

						if(Max<=Fina) {break;}

						if(Der<Izq)	{Primero--;}

						Tamanyo++;

					}


					else {break;}
			}
		}

		if(Tamanyo>=CutOff){ //Print out if enough residues in stretch.

			i=Primero+Tamanyo;
			LastTM=i;
			Numero=Primero;


			Resultado=Resultado.substr(1,Primero-1)+Resultado.substr(Primero,Tamanyo)
					+Resultado.substr(Primero+Tamanyo,LonSeq-(Primero+Tamanyo-1));

			bloc = Numero;
			Numero = Primero+Tamanyo;
			eloc = Numero;

			stringi = NeuroText.substr(10+Primero,Tamanyo) + "|" + (string)itoa(bloc) + "-" + (string)itoa(eloc) + "&";

			Tamanyo=0;
			stringf+=stringi;

			} 

			else {i=Primero+Tamanyo;}
	}
	
	free(NumRes); //Free Mapping Pointer

	stringF = stringF + "=" + stringf;
	cout << stringF;
	return 1;
}


/* Funci� ARGOS */ 

/*********************************************************
  Argos21_3.c
  --------------------------------------------------------
  generated at Tue Apr 27 19:23:39 1999
  by myNet2c.c (c) 1994 Bernward Kett
*********************************************************/


float Argos21_3(const char Frag[21]) {

	long int cSeq, cPos, member, source, unitNr;
	int this_aa;
	float sum;

	/* layer definition section (names & member units) */
	for(cSeq = 0; cSeq < 21; cSeq++) {
	  
	this_aa=aaEki[(unsigned)Frag[cSeq]-65]-1;

	for(cPos = 0; cPos < 20; cPos++){
	   	
		Units[Entrada[21*cSeq+cPos]].act = (this_aa==cPos)?1:-1;
		}

	Units[Entrada[21*cSeq+20]].act = -1;
	}

	for (member = 0; member < 20; member++) {
	  
	unitNr = Hidden1[member];
	sum = 0.0;

		for (source = 0; source < Units[unitNr].NoOfSources; source++) {
	
	  		sum += Units[Units[unitNr].sources[source]].act * Units[unitNr].weights[source];
	 }

	Units[unitNr].act = Act_TanH_Xdiv2(sum, Units[unitNr].Bias);
	}

	for (member = 0; member < 1; member++) {
	  
		unitNr = Output1[member];
	sum = 0.0;

	for (source = 0; source < Units[unitNr].NoOfSources; source++) {
		
	  	sum += Units[Units[unitNr].sources[source]].act* Units[unitNr].weights[source];
	}

		Units[unitNr].act = Act_TanH_Xdiv2(sum, Units[unitNr].Bias);

	}
	return(Units[Output2[0]].act);
}