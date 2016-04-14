D = {[0] = 8,[1]=1,[2]=2,[3]=3,[4]=4}
E = {[0] = 5,[1]=1,[2]=2,[3]=3,[4]=4}
j = 0
sum = 0
repeat 
   a = D[j]
   b = E[j]
   sum = sum + a*b
   j = j+1
until j ==4
print(sum)
