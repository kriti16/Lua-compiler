#include <stdio.h>
#include <bits/stdc++.h>
#include <map>

using namespace std;

extern "C"
char*  InputString()
{
  char* s = (char*)malloc(100);
  gets(s);//scanf("%s\n",s);
  return s;
}
extern "C"
char *createStringP(char * str)
{
  int l,i = 0;
  for(i=0;i< str[i]!= '\0';++i)
    {
      l++;
    }
  char *s = (char*)malloc(l+1);
  s[0]=str[0];
  for(i=0;i< str[i]!= '\0';++i)
    {
      s[i] = str[i];
    }
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

extern "C"
void PrintString(char *s)
{
  int i=0;
  printf("%s\n",s);
}

// int main()
// {
//    char* a = InputString();
//    char* b = InputString();
//    printf("%s",MergeString(a,b));
//    // string* c= CreateString2();
//    // cout<<*c<<endl;
// }
