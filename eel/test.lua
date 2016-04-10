z = 2
while z<100 do
   if z% 3 == 0 or z%7==0 then
      print(z)
      if z %23 == 0 then
         z = z + 10
         print(z)
         function f(x,y,z)
            x = x+ y + z
            return x
         end
         print (f(2,z,z+2))
         break
      end
   end
   z = z+1
end
