y = 2
function f1()
   y = 2
   y = 222
   do
      local y = 3333
      print(y)
   end
   print(y)
   z()
   function z()
      y = 3
      print(y)
      return 3
   end
   y = 322
   print(y)
   return y
end
print(y)
function g1()
   y = 2
   return y
end
dd = f1()
print(dd)
