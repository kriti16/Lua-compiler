#include <stdio.h>
#include <iostream>
#include <map>


extern "C"
const std::map<int,int> *  subtract(int a,int b)
{
  std::map<int,int> *first = new  std::map<int,int>;
  first->insert(std::pair<int,int>(a,b));
  //printf("%u\n",first);
  return first;
    }


extern "C"
int get(const std::map<int,int> * first,int a)
{

  int b = first->at(a);
  return b;
    }
