Z ={}
z = 2
c = 0
function isPrime(z)
   i = 2
   while i<z-1 do
      if z%i == 0 then
         return i
      else
         i = i+1
      end
   end
   return 0
end
counter = 2
scan(d)
while counter < d do
   prflg = isPrime(counter)
   if prflg == 0 then
      Z[counter] =1
   else
      Z[counter] = 0
   end
   counter = counter + 1
end
counter = 2
while counter < d do
   y = Z[counter]
   if y == 1 then
      print(counter)
   end
   counter = counter +1
end
