#!/usr/bin/perl

use CGI;
use Bio::DB::SwissProt;
use Bio::DB::GenPept;



$p = new CGI;

print $p->header, $p->start_html(-title=>'TransMem', -BGCOLOR=>'#F0F8FF'),

"<table width='100%' border='1' bgcolor='#00BFFF'><tr bgcolor='#00BFFF'><td><table width='100%' border='0'><tr bgcolor='#00BFFF'><td width='30%' align='center'><img
src='http://bioinf.uab.es/trsdb/memlogo.png' alt='Logo'></td>
	       
	       <td width='20%' align='left'>",

#Formulari
	       $p-> start_form, $p->p,
	       " <b>Name</b>", $p->br,
               $p->textfield('ID'),  $p->p,
	       " <b>ID</b>", $p->br,
               $p->textfield('ac'), $p->popup_menu(-name=>'extern', -values=>['SWISS-PROT', 'GenPept'], -default=>'SWISS-PROT'), $p->p,

	       $p->p, 
	       "<b>Min res X stretch</b>",
	       $p->textfield('tm'), $p->p,

	      
	       "</td><td width='50%' align='left'>",
	       " <b>Sequence</b>",$p->br, 
	       
               $p->textarea(-name=>'seq', -rows=>'10', -columns=>'62') ,

	       $p->br, 
	       "</td></tr><tr><td>",
	        
	       "</td><td>", 
	       $p->checkbox(-name=>'Detailed', -value=>'Detailed'),
	        	       
	       
	       "</td><td align='right'>",
	       
	       $p->submit(-value=>'TransMem!', -name=>'transmem'), "</td></tr></table></td></tr></table>" ,$p->end_form;

	       
#Per usuari


if ($p->param()) {
	
unless ($p->param('seq')=~/^\s*$/) {

	$ide = $p->param('ID');
	$seqstring = $p->param('seq');
	&process;
}

elsif (($p->param('ac')=~/^\s*$/) and ($p->param('seq')=~/^\s*$/)) {
		print "<blockquote>It appears you have entered NO sequence or ID";
	}

#De xarxa
else {
	#SWISS-PROT
	if (($p->param('extern') eq 'SWISS-PROT') and ($p->param('ac')!=~/^\s*$/)) {
		
			$sp = new Bio::DB::SwissProt;
		 	$seqi = $sp->get_Seq_by_id($p->param('ac')); 
			$seqstring = $seqi->seq();
			$id=$seqi->display_id(); $acc=$seqi->accession_number();
			$ide="$id";
			&process;
	}
	#GenPept
	elsif (($p->param('extern') eq 'GenPept') and ($p->param('ac')!=~/^\s*$/)) {
		
			$gp = new Bio::DB::GenPept;
         		$seqi = $gp->get_Seq_by_id($p->param('ac')); 
			$seqstring = $seqi->seq();
			$id=$seqi->display_id(); $acc=$seqi->accession_number();
			$ide="$id";
			&process;
	
	}
	

}
	
}


#Portada

else { print "<blockquote><p align='center'><font size=+3><b>Welcome to TransMem!</b></font></p><br />",

	"
	<font type='Arial' size=-1>
	<font size=+1><b>TransMem</b></font> is an ANN (Artificial Neural Network) based program for predicting transmembrane domains in proteins.<br /><br />",

	"<table width='100%' bgcolor='#00BFFF'><tr><td><b>Usage</b></td></tr></table> <br />",

	"- You can paste or type your sequence and giving it a name (optional).<br />
	- You can type SWISS-PROT/TREMBL (ex P08100) or GenPept (9506709) code or accession, then identification and sequence will be automatically retrieved for you.
	<br /><br />",
	"<table width='100%' bgcolor='#00BFFF'><tr><td><b>Options</b></td></tr></table> <br />",

	"- Min res X stretch: You can define a positive integer of minimum number of adjacent residues with positive score to consider having found a transmembrane domain. By default is set to 9.<br />
	- Detailed: If Detailed is checked you will get scores of every residue in your sequence.
	<br /><br />",
	
	"<table width='100%' bgcolor='#00BFFF'><tr><td><b>Bibliography</b></td></tr></table> <br />",

	"* P. Aloy, J. Cedano, B. Oliva, F.X. Avilés, and E. Querol, <i>TransMem: A neural network implemented in Excel spreadsheets for predicting transmembrane domains in proteins</i>, Computer Applications in Biosciences, 13, 231-234, 1997. 
	<br /><br />
	<p align='center'><font size=+1>Have a Nice Prediction!</font></p>
	";


print "</blockquote><hr/ ><font size=-1><p align='right'>Contact <a href='mailto:flipe\@bioinf.uab.es'>flipe\@bioinf.uab.es</a> IBB-UAB 2002</font></font></blockquote>";


print $p->end_html;


}




sub process {			
print $p->p, 
"<blockquote>
<font face='Arial' size=-1>";



$seqstring=~s/\s*//g;
chomp($seqstring);



print 	
	"<blockquote>",
	
	"<table width='100%' bgcolor='#00BFFF'><tr><td><b>Identification</b></td></tr></table> <br />",
	
	"<b>$ide</b><br /></font>";
				




	

print $p->br, "<table width='100%' bgcolor='#00BFFF'><tr><td><b>TransMem Results</b></td></tr></table><br/>";


$begin=0;
$end=0;

if ($p->param('tm')) {$entry=$p->param('tm');} #Minimum number of +NN aa to consider being a stretch
	
else {$entry=9;} #Default used as minimum

if ($p->param('Detailed') eq 'Detailed') {$check=1;} #Give detailed results if specified by user
else {$check=0;}

$strin = transmem($begin, $end, $entry, $ide, $seqstring, $check); #Get output from C++

($deta, $infos) = split (/=/, $strin); #Differentiate 2 ouputs

#Deal with output of detected stretches
(@dettm)= split (/&/, $infos);

	
foreach $i (@dettm) {

	($stretch, $rest) = split (/\|/, $i);
	push (@tm, $stretch);
	push (@restes, $rest);

}

foreach $a (@restes) {

	($com, $fin) = split (/-/, $a);
	push (@bloc, $com);
	push (@eloc, $fin);
}


#Deal with output of per aa NN info
(@detas)= split (/&/, $deta);

foreach $i (@detas) {

	($numres, $resti) = split (/\|/, $i);
	push (@numr, $numres);
	push (@restesi, $resti);

}

foreach $a (@restesi) {

	($ama, $valnn) = split (/->/, $a);
	push (@aas, $ama);
	push (@nn, $valnn);
}

$longa= @aas;

$long= @eloc;

#Print out predicted TransMembrane Stretches
print "<font type='Arial' size=-1>";
for ($c=0; $c<$long; $c++) {

	print "<b>TM</b> \: <i>$tm[$c]</i> \|\t <b>$bloc[$c]</b> => <b>$eloc[$c]</b><br />";

}
print "</font>";

#Print out detailed results if suitable
if ($check=1) {
print "<br /><hr /><font type='Arial' size=-1>";
for ($d=0; $d<$longa; $d++) {

	print "<i>$numr[$d]</i> : $aas[$d] => <b>$nn[$d]</b><br />\n";

}
print "</font>";
}

else {}

#Beginning of C++ program core
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

#define Act_TanH_Xdiv2(sum, bias)(tanh((sum + bias)/2))

using namespace std;
float Argos21_3(const char *);

SV* transmem(double beg, double fin, int ent, char* ide, char* protseq, int check) {

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
   return newSVpvf(stringF.c_str());
}


/* Funció ARGOS */ 

/*********************************************************
  Argos21_3.c
  --------------------------------------------------------
  generated at Tue Apr 27 19:23:39 1999
  by myNet2c.c (c) 1994 Bernward Kett
*********************************************************/


float Argos21_3(const char Frag[21])
{
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

#Print the end of html document
print "</blockquote><br /><hr/ ><font size=-1><p align='right'>Contact <a href='mailto:flipe\@bioinf.uab.es'>flipe\@bioinf.uab.es</a> IBB-UAB 2002</font></font></blockquote>";

}

print $p->end_html;

