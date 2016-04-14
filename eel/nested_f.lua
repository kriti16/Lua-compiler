x = 1
c = "a"
d = "v"
e = c..d
IN = "INSIDE"
PrintString(e)
function f(x)
   while x <100 do
      function g(a)
         function h(aa)
            kl = 0
            x = 0
            while x < aa do
               x = x+aa
               print(x)
            end
         return a*2
         end
         x = h(a)
         print(x)
         return x
         end
      t = g(x)
      x = x+1
   end
   return x
end

print(f(2))
