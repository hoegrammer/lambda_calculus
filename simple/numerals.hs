zero :: ((a -> a) -> a -> a)
zero f = id

--define the c_successor function
--and a generate a few integers

c_succ :: ((a -> a) -> a -> a) -> ((a -> a) -> a -> a)
c_succ n f =  f . (n f) 

one :: ((a -> a) -> a -> a) 
one = c_succ zero

two :: ((a -> a) -> a -> a)
two = c_succ one

three :: ((a -> a) -> a -> a) 
three = c_succ two 

four :: ((a -> a) -> a -> a)
four = c_succ three

--define helper functions to convert church numerals to integers
--and vice versa

church_to_int :: ((Int -> Int) -> Int -> Int) -> Int
church_to_int church = church (+1) 0

--Define addition, multiplication and exponentiation

add :: ((a -> a) -> a -> a) -> ((a -> a) -> a -> a) -> ((a -> a) -> a -> a) 
add m n f = (m f) . (n f)

mult :: ((a -> a) -> a -> a) -> ((a -> a) -> a -> a) -> ((a -> a) -> a -> a)
mult = (.)

expn = id 

--
--''' 
--Define Kleene's predeccessor function
--pair takes a selector 's' and uses it to return the first or second element of a pair 
--pzero is a pair of zeros
--pc_succ takes pair p = (a,b) to (b,c_succ(b))
--pred of n returns (n-1)
--'''
--
--pair = lambda a: lambda b: lambda s: s(a)(b)
--pzero = pair(zero)(zero)
--pc_succ = lambda p: pair(p(snd))(c_succ(p(snd)))
--pred = lambda n: n(pc_succ)(pzero)(fst)
--
--
--'''
--Create a subtraction function from the predecessor function
--sub(m)(n) == m - n
--'''
--
--sub = lambda m: lambda n: n(pred)(m)
--
--
--''' 
--Tests
--'''
--
--assert church_to_int(one) == 1
--assert church_to_int(two) == 2
--assert church_to_int(three) == 3 
--assert church_to_int(four) == 4 
--
--assert church_to_int(add(one)(one)) == 2
--assert church_to_int(mult(four)(three)) == 12
--assert church_to_int(expn(two)(three)) == 8
--
--assert church_to_int(pred(four)) == 3
--assert church_to_int(sub(four)(three)) == 1
