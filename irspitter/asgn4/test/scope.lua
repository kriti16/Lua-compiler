x = 5
function  foo()
	print(x)
	local x = 5
	do
		x = 6
		print(x)
	end
end

function bar( )
	x = x + 5
	do
		local x = 10
		print(x)
	end
	print(x)
	foo()
	local x = 10
	print(x)
end

foo()
print(x)


