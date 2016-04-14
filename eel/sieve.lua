Ques = "Enter:"
PrintString(Ques)
scan(d)
Pr = {}
do local counter = 1
   while counter <=d do
      Pr[counter] = 1
      counter = counter + 1
   end
end
current , counter = 2,2
while current < d do
   counter = current
   while counter < d do
      Pr[counter] = 2
      flag = Pr[counter]
      print(flag)
      counter = counter + current
   end
   flag = Pr[current]
   print(flag)
   while flag == 0  and current < d do
      current = current + 1
      flag = Pr[current]
      print(current)
      PrintString("HELLo")
      print(flag)
   end
   end
   

