x=1
y=2
function f(a,b)
   z = a + b
   return z
end

while x < 100 do
   y = f(x,y)
   x = x+1
   print(y)
end
print(x)
