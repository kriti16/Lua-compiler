y = 1
pp = 8
z = 0
if y == 1 then
   z = 500
   repeat
      z = z-1
      if z% 2==0 then
         pp = pp - z
      else
         function f()
            if pp %2 == 0 then
               return 3
            else
               return 4
            end
         end
         pp = pp+f()
         
      end
      until z<0
   
   y = 3
end
p = y + z + pp
print(pp)
