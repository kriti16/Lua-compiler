#include <stdio.h>
#include <map>
#include <iostream>
#include <string>
using namespace std;
extern "C"
map<string,int> *  CreateDict()
{
  map<string,int> *temp = new  map<string,int>;
  return temp;
}


extern "C"
map<string,int> * insertDict(map<string,int> * temp,char *a,int b)
{
  string R = a;
  temp->insert( pair<string,int>(R,b) );
  //cout<<R<<"Hello"<<endl;
  return temp;
}


extern "C"
int getDict(std::map<string,int> * temp,char *a)
{
  string R = a;
  //cout<<R<<"JELO"<<endl;
  int  b = temp->at(R);
  return b;
}
