import Test.HUnit

false :: a -> a -> a
false x y = y

true :: a -> a -> a
true x y = x

c_not :: ((a -> a -> a) -> (a -> a -> a) -> (a -> a -> a)) -> a -> a -> a
c_not x = x false true

c_or :: ((a -> a -> a) -> (a -> a -> a) -> (a -> a -> a)) -> ((a -> a -> a) -> (a -> a -> a) -> (a -> a -> a)) -> a -> a -> a 
c_or x y =  x true (y true false)

c_and :: ((a -> a -> a) -> (a -> a -> a) -> (a -> a -> a)) -> ((a -> a -> a) -> (a -> a -> a) -> (a -> a -> a)) -> a -> a -> a 
c_and x y = x (y true false) false

if_then_else = id  -- if_then_else test if_thing else_thing = test if_thing else_thing

--define a helper function 

church_to_boolean :: (Bool -> Bool -> Bool) -> Bool
church_to_boolean cb = cb True False

--Tests

test1 = TestCase (assertEqual "church_to_boolean false" (False) (church_to_boolean false))
test2 = TestCase (assertEqual "church_to_boolean true" (True) (church_to_boolean true))

test3 = TestCase (assertEqual "not true is false" (False) (church_to_boolean (c_not true)))
test4 = TestCase (assertEqual "not false is true" (True) (church_to_boolean (c_not false)))

test5 = TestCase (assertEqual "true or true is true" (True) (church_to_boolean (c_or true true)))
test6 = TestCase (assertEqual "true or false is true" (True) (church_to_boolean (c_or true false)))
test7 = TestCase (assertEqual "false or false is false" (False) (church_to_boolean (c_or false false)))
test8 = TestCase (assertEqual "false or true is true" (True) (church_to_boolean (c_or false true)))

test9 = TestCase (assertEqual "true and true is true" (True) (church_to_boolean (c_and true true)))
testa = TestCase (assertEqual "true and false is false" (False) (church_to_boolean (c_and true false)))
testb = TestCase (assertEqual "false and false is false" (False) (church_to_boolean (c_and false false)))
testc = TestCase (assertEqual "false and true is false" (False) (church_to_boolean (c_and false true)))

testd = TestCase (assertEqual "if_then_else returns if_thing when test is true" (True) (church_to_boolean (if_then_else true true false)))
teste = TestCase (assertEqual "if_then_else return else_thing when test is false" (False) (church_to_boolean (if_then_else false true false)))

tests = TestList [
  TestLabel "test1" test1 , 
  TestLabel "test2" test2 , 
  TestLabel "test3" test3, 
  TestLabel "test4" test4, 
  TestLabel "test5" test5, 
  TestLabel "test6" test6, 
  TestLabel "test7" test7, 
  TestLabel "test8" test8,
  TestLabel "test9" test9,
  TestLabel "testa" testa,
  TestLabel "testb" testb,
  TestLabel "testc" testc,
  TestLabel "testd" testd,
  TestLabel "teste" teste ]
