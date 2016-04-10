function f(x,y)
   d = x+ y
   print(x)
   print(y)
   if x == 10 then
      return x
   end
   d = f(x+1,y+1)
   print(d)
   
   return d
end
print(f(2,88))
