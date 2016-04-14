PrintString("Number:")
scan(d)
counter = 0
Grade ={}
Roll = {}
HomeTown = {}
NAME = "Name:"
GRADE = "Grade:"
ROLL = "Roll:"
Test = "Testing!"
Exit = "Exit(0/1)?"
gen = "Generate(0/1)?"
PrintString(Exit)
counter = 0
while counter<d do
PrintString(NAME)
nn = InputString()
PrintString(ROLL)
scan(r)
Roll[nn]=r
PrintString(Exit)
scan(e)
if e == 0 then
   break
end
counter = counter + 1
end
PrintString(Test)
PrintString(NAME)
nn = InputString()
gr = Roll[nn]
print(gr)
PrintString(gen)
