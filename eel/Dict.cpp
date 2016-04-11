#include <stdio.h>
#include <bits/stdc++.h>
#include <map>

using namespace std;
extern "C"
map<int,int> *  CreateDict()
{
  map<int,int> *temp = new  map<int,int>;
  return temp;
    }


extern "C"
map<int,int> * insertDict(map<int,int> * temp,int a,int b)
{
  temp->insert( pair<int,int>(a,b) );
  cout<< temp->at(a)<<endl;
  return temp;
    }


extern "C"
int get(std::map<int,int> * temp,int a)
{

  int b = temp->at(a);
  return b;
    }
