package TransMem;

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(process);


sub process {

	my $seqid = shift;
	my $protseq = shift;
	
	my $begin=0;
	my $end=0;
	my $check = 0;
	my $ent = 9;
	
	my $string;

	#Beginning of C++ program core
	use Inline CPP => Config =>
		           INC => "-I ./";
	use Inline CPP => <<'ENDCPP';

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
	#include <unistd.h>

	#define Act_TanH_Xdiv2(sum, bias)(tanh((sum + bias)/2))

	const int fillX = 10; 

	using namespace std;

	float Argos21_3(const char *);

	SV* transmem( double beg, double fin, int ent, char* seqid, char* protseq, int check ) {

		string Neuras(string, string);

		int numf, dec, sig;
		string NeuroText, stringi, stringf, sbloc, seloc, sres, Numstring, Resstring, Detstring, stringF, ssign;

		// Control variables

		NeuroText= protseq;	// Sequence

		int i, LonSeq, Primero, Tamanyo;
		string Salida,Resultado;

		int Numero, bloc, eloc;
		float *NumRes;
		float Inic, Fina, Der, Izq, Max;
		int LastTM, CutOff;

		//Control variables are assigned
		Inic=beg;
		Fina=fin;
		CutOff=ent;

		//Array of mappings to NN made from seq length
		LonSeq = NeuroText.length(); 
		NumRes = (float *)calloc(LonSeq+1,sizeof(float)); 

		Resultado = NeuroText;

		// cout << ID + "\n" + NeuroText+ "\n" <<LonSeq << " residues\n\n"; //Print out ID, sequence and num of residues.

		int x;
		for ( x = 0; x < fillX; x++ ) {
	
			NeuroText = "X"+NeuroText+"X";
		}


		// Begin iteration for sequence

		for(i=1;i<LonSeq;i++){

			NumRes[i]=Argos21_3(NeuroText.substr((long int)i,21).c_str()); // Sent to Argos
	
			if(check==1){

				// Display NN mappings
				Numero = i;
		
				Numstring = (string)itoa(Numero);
				Resstring = (string)fcvt(NumRes[i], numf, &dec, &sig);
		
				if (sig==1) {ssign="-";}
				if (sig==0) {ssign="+";}
		
				Detstring = "#"+ (string)seqid + "@" + Numstring + "|" + NeuroText.substr((long int)(i+fillX),1)+"->" + ssign + (string)itoa(dec) + "." + Resstring + "\n";
		
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

			if(Tamanyo>=CutOff) { //Print out if enough residues in stretch.

				i=Primero+Tamanyo;
				LastTM=i;
				Numero=Primero;
		
				int endIter;
				endIter = LonSeq-(Primero+Tamanyo-1);
			
				if ( LonSeq < endIter+Resultado.length() ) {
			
						Resultado=Resultado.substr(1,Primero-1)+Resultado.substr(Primero,Tamanyo)+Resultado.substr(Primero+Tamanyo,endIter);

						bloc = Numero;
						Numero = Primero+Tamanyo;
						eloc = Numero;
			
						stringi = (string)seqid + "\t" + NeuroText.substr(fillX+Primero,Tamanyo) + "\t" + (string)itoa(bloc) + "\t" + (string)itoa(eloc) + "\n";

						Tamanyo=0;
						stringf+=stringi;
				}

			} 

			else {i=Primero+Tamanyo;}
		}
	
		free(NumRes); //Free Mapping Pointer

		stringF = stringF + stringf;
		// return stringF;
		return newSVpvf(stringF.c_str());

	}


	/* Funció ARGOS */ 

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
	
ENDCPP
	
	$string = transmem($begin, $end, $ent, $seqid, $protseq, $check) ; #Get output from C++
	return $string; 
}
