function isPrime(n)
	if n == 1 then
		return 0
	else
		i = 2
		prime = 1
		while(i*i<=n) do	
			if n%i == 0 then
				prime = 0
				break
			end
			i = i + 1
		end
	end
	return prime
end

x = 5
if isPrime(x)==1 then
	print(1)
else
	print(0)
end
d = {}
