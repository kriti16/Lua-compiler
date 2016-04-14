scan(x)
scan(y)
function add(x,y)
   return x+y
end
function sub(x,y)
   return x-y
end
function mult(x,y)
   return add(x,y)*sub(x,y)
end
print(add(x,y))
print(sub(x,y))
print(mult(x,y))
