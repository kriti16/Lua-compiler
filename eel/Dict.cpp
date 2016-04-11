#include <stdio.h>
#include <iostream>
#include <map>

using namespace std;
extern "C"
std::map<int,int> *  CreateDict()
{
  map<int,int> *first = new  map<int,int>;
  return first;
    }


extern "C"
int insert(map<int,int> * first,int a,int b)
{

  first->insert( pair<int,int>(a,b) );
  return 1;
    }


extern "C"
int get(std::map<int,int> * first,int a)
{

  int b = first->at(a);
  return b;
    }
