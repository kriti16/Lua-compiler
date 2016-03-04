function get_all_factors(number, bun)
  local factors =  {}
  for possible_factor=1, math.sqrt(number), 1 do
     local remainder = number%possible_factor
    
     if remainder == 0 then
       local factor, factor_pair = possible_factor, number/possible_factor
      table.insert(factors, factor )
      a = 3
      if factor ~= factor_pair then
         table.insert(factors, factor_pair)
     end
     end
  end
  -- table.sort(factors)
  -- return factors
  end

--The Meaning of the Universe is 42. Let's find all of the factors driving the Universe.

