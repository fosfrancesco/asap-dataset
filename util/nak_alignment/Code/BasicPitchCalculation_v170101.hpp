/*
Copyright 2019 Eita Nakamura

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef BASICPITCHCALCULATION_HPP
#define BASICPITCHCALCULATION_HPP

#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>
#include<stdio.h>
#include<stdlib.h>
#include<cmath>
#include<cassert>
#include<algorithm>
using namespace std;

inline string OldSitchToSitch(string sitch_old){
	for(int i=0;i<sitch_old.size();i+=1){
		if(sitch_old[i]=='+'){sitch_old[i]='#';}
		if(sitch_old[i]=='-'){sitch_old[i]='b';}
	}//endfor i
	return sitch_old;
}//end OldSitchToSitch

inline string SitchToOldSitch(string sitch){
	for(int i=0;i<sitch.size();i+=1){
		if(sitch[i]=='#'){sitch[i]='+';}
		if(sitch[i]=='b'){sitch[i]='-';}
	}//endfor i
	return sitch;
}//end SitchToOldSitch

inline string PitchToSitch(int p){//pithc to spelled pitch (sitch)
	int q=(p+120)%12;
	string qstr;
	stringstream ss;
	switch(q){
		case 0 : qstr="C"; break;
		case 1 : qstr="C#"; break;
		case 2 : qstr="D"; break;
		case 3 : qstr="Eb"; break;
		case 4 : qstr="E"; break;
		case 5 : qstr="F"; break;
		case 6 : qstr="F#"; break;
		case 7 : qstr="G"; break;
		case 8 : qstr="G#"; break;
		case 9 : qstr="A"; break;
		case 10 : qstr="Bb"; break;
		case 11 : qstr="B"; break;
	}//endswitch
	ss.str(""); ss<<qstr<<(p/12-1);
	return ss.str();
}//end PitchToSitch

inline string PitchToOldSitch(int p){//pithc to spelled pitch (sitch)
	int q=(p+120)%12;
	string qstr;
	stringstream ss;
	switch(q){
		case 0 : qstr="C"; break;
		case 1 : qstr="C+"; break;
		case 2 : qstr="D"; break;
		case 3 : qstr="E-"; break;
		case 4 : qstr="E"; break;
		case 5 : qstr="F"; break;
		case 6 : qstr="F+"; break;
		case 7 : qstr="G"; break;
		case 8 : qstr="G+"; break;
		case 9 : qstr="A"; break;
		case 10 : qstr="B-"; break;
		case 11 : qstr="B"; break;
	}//endswitch
	ss.str(""); ss<<qstr<<(p/12-1);
	return ss.str();
}//end PitchToOldSitch

inline int SitchToPitch(string sitch){
	int p_rel,p;
	if(sitch[0]=='C'){p_rel=60;
	}else if(sitch[0]=='D'){p_rel=62;
	}else if(sitch[0]=='E'){p_rel=64;
	}else if(sitch[0]=='F'){p_rel=65;
	}else if(sitch[0]=='G'){p_rel=67;
	}else if(sitch[0]=='A'){p_rel=69;
	}else if(sitch[0]=='B'){p_rel=71;
	}//endif
	sitch.erase(sitch.begin());
	int oct=sitch[sitch.size()-1]-'0';
	sitch.erase(sitch.end()-1);
	p=p_rel+(oct-4)*12;
	if(sitch==""){p+=0;
	}else if(sitch=="#"){p+=1;
	}else if(sitch=="##"){p+=2;
	}else if(sitch=="b"){p-=1;
	}else if(sitch=="bb"){p-=2;
	}else if(sitch=="+"){p+=1;
	}else if(sitch=="++"){p+=2;
	}else if(sitch=="-"){p-=1;
	}else if(sitch=="--"){p-=2;
	}//endif
	return p;
}//end 

inline int SitchClassToPitchClass(string sitch){
	int p_rel,p;
	if(sitch[0]=='C'){p_rel=0;
	}else if(sitch[0]=='D'){p_rel=2;
	}else if(sitch[0]=='E'){p_rel=4;
	}else if(sitch[0]=='F'){p_rel=5;
	}else if(sitch[0]=='G'){p_rel=7;
	}else if(sitch[0]=='A'){p_rel=9;
	}else if(sitch[0]=='B'){p_rel=11;
	}//endif
	sitch.erase(sitch.begin());
	p=p_rel+12;
	if(sitch==""){p+=0;
	}else if(sitch=="#"){p+=1;
	}else if(sitch=="##"){p+=2;
	}else if(sitch=="b"){p-=1;
	}else if(sitch=="bb"){p-=2;
	}else if(sitch=="+"){p+=1;
	}else if(sitch=="++"){p+=2;
	}else if(sitch=="-"){p-=1;
	}else if(sitch=="--"){p-=2;
	}//endif
	return p%12;
}//end 

inline string PitchClassToSitchClass(int pc){
	int q=(pc+120)%12;
	string qstr;
	switch(q){
		case 0 : qstr="C"; break;
		case 1 : qstr="C#"; break;
		case 2 : qstr="D"; break;
		case 3 : qstr="Eb"; break;
		case 4 : qstr="E"; break;
		case 5 : qstr="F"; break;
		case 6 : qstr="F#"; break;
		case 7 : qstr="G"; break;
		case 8 : qstr="Ab"; break;
		case 9 : qstr="A"; break;
		case 10 : qstr="Bb"; break;
		case 11 : qstr="B"; break;
	}//endswitch
	return qstr;
}//end PitchClassToSitchClass

inline string PitchClassToOldSitchClass(int pc){
	int q=(pc+120)%12;
	string qstr;
	switch(q){
		case 0 : qstr="C"; break;
		case 1 : qstr="C+"; break;
		case 2 : qstr="D"; break;
		case 3 : qstr="E-"; break;
		case 4 : qstr="E"; break;
		case 5 : qstr="F"; break;
		case 6 : qstr="F+"; break;
		case 7 : qstr="G"; break;
		case 8 : qstr="A-"; break;
		case 9 : qstr="A"; break;
		case 10 : qstr="B-"; break;
		case 11 : qstr="B"; break;
	}//endswitch
	return qstr;
}//end PitchClassToOldSitchClass

inline int SitchToSitchHeight(string sitch){
	int oct=sitch[sitch.size()-1]-'0';
	char sitchClass=sitch[0];
	int ht;
	if(sitchClass=='C'){ht=0;
	}else if(sitchClass=='D'){ht=1;
	}else if(sitchClass=='E'){ht=2;
	}else if(sitchClass=='F'){ht=3;
	}else if(sitchClass=='G'){ht=4;
	}else if(sitchClass=='A'){ht=5;
	}else if(sitchClass=='B'){ht=6;
	}else{ht=0;
	}//endif
	return ht+7*(oct-4);
}//end SitchToSitchHeight

inline int SitchToAcc(string sitch){
	string accLab=sitch.substr(1,sitch.size()-2);
	if(accLab==""){return 0;
	}else if(accLab=="#"){return 1;
	}else if(accLab=="##"){return 2;
	}else if(accLab=="b"){return -1;
	}else if(accLab=="bb"){return -2;
	}else if(accLab=="+"){return 1;
	}else if(accLab=="++"){return 2;
	}else if(accLab=="-"){return -1;
	}else if(accLab=="--"){return -2;
	}else{return 0;
	}//endif
}//end SitchToAcc

inline string KeyFromKeySignature(int key_fifth,string key_mode){
	string key="Cmaj";
	if(key_mode=="major" && key_fifth==-7){key="Cbmaj";
	}else if(key_mode=="major" && key_fifth==-6){key="Gbmaj";
	}else if(key_mode=="major" && key_fifth==-5){key="Dbmaj";
	}else if(key_mode=="major" && key_fifth==-4){key="Abmaj";
	}else if(key_mode=="major" && key_fifth==-3){key="Ebmaj";
	}else if(key_mode=="major" && key_fifth==-2){key="Bbmaj";
	}else if(key_mode=="major" && key_fifth==-1){key="Fmaj";
	}else if(key_mode=="major" && key_fifth==0){key="Cmaj";
	}else if(key_mode=="major" && key_fifth==1){key="Gmaj";
	}else if(key_mode=="major" && key_fifth==2){key="Dmaj";
	}else if(key_mode=="major" && key_fifth==3){key="Amaj";
	}else if(key_mode=="major" && key_fifth==4){key="Emaj";
	}else if(key_mode=="major" && key_fifth==5){key="Bmaj";
	}else if(key_mode=="major" && key_fifth==6){key="F#maj";
	}else if(key_mode=="major" && key_fifth==7){key="C#maj";
	}else if(key_mode=="minor" && key_fifth==-7){key="Abmin";
	}else if(key_mode=="minor" && key_fifth==-6){key="Ebmin";
	}else if(key_mode=="minor" && key_fifth==-5){key="Bbmin";
	}else if(key_mode=="minor" && key_fifth==-4){key="Fmin";
	}else if(key_mode=="minor" && key_fifth==-3){key="Cmin";
	}else if(key_mode=="minor" && key_fifth==-2){key="Gmin";
	}else if(key_mode=="minor" && key_fifth==-1){key="Dmin";
	}else if(key_mode=="minor" && key_fifth==0){key="Amin";
	}else if(key_mode=="minor" && key_fifth==1){key="Emin";
	}else if(key_mode=="minor" && key_fifth==2){key="Bmin";
	}else if(key_mode=="minor" && key_fifth==3){key="F#min";
	}else if(key_mode=="minor" && key_fifth==4){key="C#min";
	}else if(key_mode=="minor" && key_fifth==5){key="G#min";
	}else if(key_mode=="minor" && key_fifth==6){key="D#min";
	}else if(key_mode=="minor" && key_fifth==7){key="A#min";
	}//endif
	return key;
}//end KeyFromKeySignature

#endif // BASICPITCHCALCULATION_HPP





























