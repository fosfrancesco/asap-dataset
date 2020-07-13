/*
Copyright 2019 Eita Nakamura

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef BasicCalculation_HPP
#define BasicCalculation_HPP

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

inline int gcd(int m, int n){
	if(0==m||0==n){return 0;}
	while(m!=n){if(m>n){m=m-n;}else{n=n-m;}}//endwhile
	return m;
}//end gcd
inline int lcm(int m,int n){
	if (0==m||0==n){return 0;}
	return ((m/gcd(m,n))*n);//lcm=m*n/gcd(m,n)
}//end lcm

inline double LogAdd(double d1,double d2){
	//log(exp(d1)+exp(d2))=log(exp(d1)(1+exp(d2-d1)))
	if(d1>d2){
//		if(d1-d2>20){return d1;}
		return d1+log(1+exp(d2-d1));
	}else{
//		if(d2-d1>20){return d2;}
		return d2+log(1+exp(d1-d2));
	}//endif
}//end LogAdd
inline void Norm(vector<double>& vd){
	double sum=0;
	for(int i=0;i<vd.size();i+=1){
		sum+=vd[i];
//		if(vd[i]<0){cout<<"negative weight!"<<endl;}
	}//endif
	for(int i=0;i<vd.size();i+=1){vd[i]/=sum;}
	return;
}//end Norm
inline void Lognorm(vector<double>& vd){
	double tmpd=vd[0];
	for(int i=0;i<vd.size();i+=1){if(vd[i]>tmpd){tmpd=vd[i];}}//endfor i
	for(int i=0;i<vd.size();i+=1){vd[i]-=tmpd;}//endfor i
	tmpd=0;
	for(int i=0;i<vd.size();i+=1){tmpd+=exp(vd[i]);}//endfor i
	tmpd=log(tmpd);
	for(int i=0;i<vd.size();i+=1){vd[i]-=tmpd;if(vd[i]<-200){vd[i]=-200;}}//endfor i
}//end Lognorm

inline double Average(vector<double>& vd){
	assert(vd.size()>0);
	double sum=0;
	for(int i=0;i<vd.size();i+=1){
		sum+=vd[i];
	}//endfor i
	return sum/double(vd.size());
}//end Average

inline double StDev(vector<double>& vd){
	assert(vd.size()>1);
	double ave=Average(vd);
	double sum=0;
	for(int i=0;i<vd.size();i+=1){
		sum+=pow(vd[i]-ave,2.);
	}//endfor i
	return pow(sum/double(vd.size()-1),0.5);
}//end StDev

inline int SampleDistr(vector<double> &p){
	double val=(1.0*rand())/(1.0*RAND_MAX);
	for(int i=0;i<p.size()-1;i+=1){
		if(val<p[i]){return i;
		}else{val-=p[i];
		}//endif
	}//endfor i
	return p.size()-1;
}//end SampleDistr

inline double RandDouble(){
	return (1.0*rand())/(1.0*RAND_MAX);
}//end

class Pair{
public:
	int ID;
	double value;
};//endclass Pair

class MorePair{
public:
	bool operator()(const Pair& a, const Pair& b){
		if(a.value > b.value){
			return true;
		}else{//if a.value <= b.value
			return false;
		}//endif
	}//end operator()
};//end class MorePair
//sort(pairs.begin(), pairs.end(), MorePair());

//From Prob_v160925.hpp
template <typename T> class Prob{
public:
	vector<double> P;
	vector<double> LP;
	vector<T> samples;

	Prob(){
	}//end Prob
	Prob(Prob<T> const & prob_){
		P=prob_.P;
		LP=prob_.LP;
		samples=prob_.samples;
	}//end Prob

	~Prob(){
	}//end ~Prob

	Prob& operator=(const Prob<T> & prob_){
		P=prob_.P;
		LP=prob_.LP;
		samples=prob_.samples;
		return *this;
	}//end =

	void Print(){
		for(int i=0;i<P.size();i+=1){
cout<<i<<"\t"<<samples[i]<<"\t"<<P[i]<<"\t"<<LP[i]<<endl;
		}//endfor i
	}//end Print

	void Normalize(){
		Norm(P);
		PToLP();
	}//end Normalize

	void LogNormalize(){
		Lognorm(LP);
		LPToP();
	}//end Normalize

	void PToLP(){
		LP.clear();
		LP.resize(P.size());
		for(int i=0;i<P.size();i+=1){
			LP[i]=log(P[i]);
		}//endfor i
	}//end PToLP

	void LPToP(){
		P.clear();
		P.resize(LP.size());
		for(int i=0;i<LP.size();i+=1){
			P[i]=exp(LP[i]);
		}//endfor i
	}//end LPToP

	T Sample(){
		return samples[SampleDistr(P)];
	}//end Sample

	void Resize(int _size){
		P.clear(); LP.clear(); samples.clear();
		P.resize(_size);
		LP.resize(_size);
		samples.resize(_size);
	}//end Resize

	void Assign(int _size,double value){
		P.clear(); LP.clear(); samples.clear();
		P.assign(_size,value);
		LP.resize(_size);
		samples.resize(_size);
	}//end Assign

	double MaxP(){
		double max=P[0];
		for(int i=1;i<P.size();i+=1){
			if(P[i]>max){max=P[i];}
		}//endfor i
		return max;
	}//end MaxValue

	void Randomize(){
		for(int i=0;i<P.size();i+=1){
			P[i]=(1.0*rand())/(1.0*RAND_MAX);
		}//endfor i
		Normalize();
	}//end Randomize

	void Sort(){
		vector<Pair> pairs;
		Pair pair;
		for(int i=0;i<P.size();i+=1){
			pair.ID=i;
			pair.value=P[i];
			pairs.push_back(pair);
		}//endfor i
		stable_sort(pairs.begin(), pairs.end(), MorePair());

		Prob<T> tmpProb;
		tmpProb=*this;
		for(int i=0;i<P.size();i+=1){
			P[i]=tmpProb.P[pairs[i].ID];
			samples[i]=tmpProb.samples[pairs[i].ID];
		}//endfor i
		PToLP();

	}//end Sort

	double Entropy(){
		double ent=0;
		for(int i=0;i<P.size();i+=1){
			if(P[i]<1E-10){continue;}
			ent+=-P[i]*log(P[i]);
		}//endfor i
		return ent;
	}//end Entropy

};//endclass Prob


#endif // BasicCalculation_HPP
