z = 0
D={}
dd = "PQRST"
t = InputString()
PrintString(dd)
while z < 20 do
   D[z]=z
   print(z)
   z  = z+1
end
p = 3
z = z-3
hh = D[z]
if z > 0 then
   print(hh)
else
   print(hh + 1)
end
print(z)
PrintString(t)
ss = MergeString(t,dd)
PrintString(ss)
