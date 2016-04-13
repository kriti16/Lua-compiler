#include <bits/stdc++.h>
//#include <stdio.h>
#include <map>
//#include <cstdlib>
//#include <math.h>

using namespace std;

extern "C"
char*  InputString()
{
  char* s = (char*)malloc(100);
  gets(s);//scanf("%s\n",s);
  return s;
}
extern "C"
char *createStringP(char *str)
{
  int l=0,i = 0;
for(i=0; (int)str[i]!='\0';++i)
    {
//cout<<str[i]<<endl;
      l++;
    }
char *s = (char *)malloc(l+1);
//cout<<str<<"Reading"<<l<<endl;
for(int i =0 ;i<l;i++)
  {
s[i] = str[i];
}
s[l]='\0';


//cout<<s<<"Before"<<str<<endl;
  return s;
}

extern "C"
char* MergeString(char* b, char* a)
{
  int i = strlen(a);
  int j = strlen(b);
  char* s = (char*)malloc(100);
  memcpy(s,b,j);
  memcpy(s + j, a, i);
  s[i + j] = '\0';
  return s;
}

extern "C"
void PrintString(char *s)
{
  // int i=0;
  printf("%s\n",s);
}
extern "C"

const char *itoa(int a)
{
/*cout<<a<<"HelloString"<<endl;
  int l = ceil(log10(a));
cout<<l<<"leng";
  char *s = (char*)malloc(l);
  while(l>0)
    {
      s[l] = (char)(a%10);
      a /= 10;
      l --;
    }
*/
string sa = to_string(a);
char const * str = sa.c_str();
  return str;
}
// int main()
// {
//    char* a = InputString();
//    char* b = InputString();
//    printf("%s",MergeString(a,b));
//    // string* c= CreateString2();
//    // cout<<*c<<endl;
// }
