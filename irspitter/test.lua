h = 3333
function f(jj)
   j = 2
   if j > 1 then
      h = 2
   elseif j >3 then
      function g()
         t = 2
         if t == 2 then
            k = 2
            return k
         else
            k = 4
         end
         return g(k)
      end
      h = g()
   else
      h = 3
   end
   return h
end
dd = f(h)
print(dd)
