function complex.to( num )
   -- check for table type
   if type( num ) == "table" then
      -- check for a complex number
      if getmetatable( num ) == complex_meta then
         return num
      end
      local real,imag = tonumber( num[1] ),tonumber( num[2] )
      if real and imag then
         return setmetatable( { real,imag }, complex_meta )
      end
      return
   end
   -- check for number
   local isnum = tonumber( num )
   if isnum then
      return setmetatable( { isnum,0 }, complex_meta )
   end
