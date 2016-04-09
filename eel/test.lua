y = 2
pp = 0
if y == 1 then
   z = 2
   y = 4
else
   z = 500
   while z>0 do
      pp = pp + 1
      z = z-1
      print(z)
   end
   y = 3
end
p = y + z + pp
print(pp)
