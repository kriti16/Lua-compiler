#include <stdio.h>
#include <bits/stdc++.h>
#include <map>

using namespace std;

extern "C"
char*  InputString()
{
  char* s = (char*)malloc(100);
  scanf("%s",s);
  return s;
}

extern "C"
char* MergeString(char* a, char* b)
{
  int i = strlen(a);
  int j = strlen(b);
  // cout<<i<<" "<<j<<endl;
  char* s = (char*)malloc(100);
  memcpy(s,a,i);
  memcpy(s + i, b, j);
  s[i + j] = '\0';
  return s;
}

// int main()
// {
//    char* a = InputString();
//    char* b = InputString();
//    printf("%s",MergeString(a,b));
//    // string* c= CreateString2();
//    // cout<<*c<<endl;
// }