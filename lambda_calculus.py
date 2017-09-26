#!/usr/bin/env python

'''
Another go  with Lambda calculus
This time though with changes to Booleans, wrapping them in additional lambda
to make them lazy evaluated. 
'''

'''
Booleans
'''

TRUE = lambda x: lambda y: x(lambda z: z)
FALSE = lambda x: lambda y: y(lambda z: z)

NOT = lambda x: x(lambda _: FALSE)(lambda _: TRUE)
OR = lambda x: lambda y: x(lambda _: TRUE)(lambda _: y(lambda _: TRUE)(lambda _: FALSE))
AND = lambda x: lambda y: x(lambda _: y(lambda _: TRUE)(lambda _: FALSE))(lambda _: FALSE)

IF = lambda c: lambda t: lambda e: c(t)(e)

'''
Boolean Tests
'''

assert TRUE(lambda _: True)(lambda _: False) == True
assert FALSE(lambda _: True)(lambda _: False) == False
assert NOT(TRUE)(lambda _: True)(lambda _: False) == False
assert NOT(FALSE)(lambda _: True)(lambda _: False) == True

assert OR(TRUE)(TRUE)(lambda _: True)(lambda _: False) == True
assert OR(TRUE)(FALSE)(lambda _: True)(lambda _: False) == True
assert OR(FALSE)(TRUE)(lambda _: True)(lambda _: False) == True
assert OR(FALSE)(FALSE)(lambda _: True)(lambda _: False) == False

assert AND(TRUE)(TRUE)(lambda _: True)(lambda _: False) == True
assert AND(TRUE)(FALSE)(lambda _: True)(lambda _: False) == False
assert AND(FALSE)(TRUE)(lambda _: True)(lambda _: False) == False
assert AND(FALSE)(FALSE)(lambda _: True)(lambda _: False) == False

assert IF(TRUE)(lambda _: "Yes")(lambda _: "No") == "Yes"
assert IF(FALSE)(lambda _: "Yes")(lambda _: "No") == "No"

''' 
Natural Numbers
'''

ZERO = lambda x: lambda y: y
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

ONE = SUCC(ZERO)
TWO = SUCC(SUCC(ZERO))
THREE = SUCC(SUCC(SUCC(ZERO)))
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
SIX = SUCC(FIVE)
SEVEN = SUCC(SIX)
EIGHT = SUCC(SEVEN)
NINE = SUCC(EIGHT)
TEN = SUCC(NINE)

''' 
Math on Natural Numbers
'''

ADD = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
ADD = lambda m : lambda n: lambda x: lambda y: (m)(SUCC)(n)(x)(y)
MULT = lambda m: lambda n: lambda f: lambda x: m(n(f))(x)

'''
Minus via Kleene's Predecessor Function
'''

PAIR = lambda a: lambda b: lambda s: s(a)(b)
FST = lambda x: lambda y: x
SND = lambda x: lambda y: y

ZZ = PAIR(ZERO)(ZERO)
PSUCC = lambda p: PAIR(p(SND))(SUCC(p(SND)))
PRED = lambda n: n(PSUCC)(ZZ)(FST)

MINUS = lambda m: lambda n: n(PRED)(m)

'''
Integer Tests
'''

assert ZERO(lambda x: x+1)(0) == 0
assert ONE(lambda x: x+1)(0) == 1
assert TWO(lambda x: x+1)(0) == 2

assert ADD(ONE)(ONE)(lambda x: x+1)(0) == 2
assert ADD(ONE)(TWO)(lambda x: x+1)(0) == 3
assert ADD(TWO)(ONE)(lambda x: x+1)(0) == 3
assert ADD(TWO)(TWO)(lambda x: x+1)(0) == 4

assert MULT(THREE)(TWO)(lambda x: x+1)(0) == 6
assert MULT(TWO)(THREE)(lambda x: x+1)(0) == 6

assert PRED(THREE)(lambda x: x+1)(0) == 2
assert PRED(FOUR)(lambda x: x+1)(0) == 3

assert MINUS(FOUR)(ONE)(lambda x: x+1)(0) == 3 
assert MINUS(FOUR)(THREE)(lambda x: x+1)(0) == 1


'''
Comparisons
'''

IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
EQ = lambda m: lambda n: AND(IS_ZERO(MINUS(m)(n)))(IS_ZERO(MINUS(n)(m)))
GT = lambda m: lambda n: AND(IS_ZERO(MINUS(m)(n)))(NOT(IS_ZERO(MINUS(n)(m)))) 
LT = lambda m: lambda n: AND(NOT(IS_ZERO(MINUS(m)(n))))(IS_ZERO(MINUS(n)(m))) 
GE = lambda m: lambda n: NOT(LT(m)(n))

'''
Comparison Tests
'''

assert IS_ZERO(ZERO)(lambda _: True)(lambda _: False) == True
assert IS_ZERO(ONE)(lambda _: True)(lambda _: False) == False
assert IS_ZERO(TWO)(lambda _: True)(lambda _: False) == False
assert IF(IS_ZERO(ZERO))(lambda _: "Yes")(lambda _: "No") == "Yes"
assert IF(IS_ZERO(ONE))(lambda _: "Yes")(lambda _: "No") == "No"

assert EQ(ONE)(ONE)(lambda _: True)(lambda _: False) == True
assert EQ(SUCC(SUCC(SUCC(SUCC(ZERO)))))(ADD(TWO)(TWO))(lambda _: True)(lambda _: False) == True

assert LT(FOUR)(THREE)(lambda _: True)(lambda _: False) == True
assert LT(THREE)(FOUR)(lambda _: True)(lambda _: False) == False
assert LT(THREE)(THREE)(lambda _: True)(lambda _: False) == False

assert GT(FOUR)(THREE)(lambda _: True)(lambda _: False) == False
assert GT(THREE)(FOUR)(lambda _: True)(lambda _: False) == True
assert GT(THREE)(THREE)(lambda _: True)(lambda _: False) == False

assert GE(THREE)(THREE)(lambda _: True)(lambda _: False) == True
assert GE(THREE)(TWO)(lambda _: True)(lambda _: False) == False
assert GE(THREE)(FOUR)(lambda _: True)(lambda _: False) == True

'''
Recursive Functions
Requires the Z combinator
'''

Z = lambda f: (lambda x: f(lambda y: (x)(x)(y)))(lambda x: f(lambda y: (x)(x)(y)))
g = lambda f: lambda n: IF(IS_ZERO(n))(lambda _: ONE)(lambda _: (MULT(n)(f(PRED(n)))))

FACTORIAL = lambda n: Z(g)(n)

fi = lambda f: lambda m: IF(OR(IS_ZERO(m))(IS_ZERO(PRED(m))))(lambda _: ONE)(lambda _: ADD(f(PRED(m)))(f(PRED(PRED(m)))))
FIBONACCI = lambda n: Z(fi)(n)


# Divide
# Variable "c" counts recursion depth as we recursively subtract b from a 
DIV = lambda f: lambda c: lambda a: lambda b: IF(GT)(a)(b)(lambda _: c)(lambda _: f(SUCC(c))(MINUS(a)(b))(b))
DIVIDE = lambda a: lambda b: Z(DIV)(ZERO)(a)(b)


REM = lambda f: lambda a: lambda b: IF(GT)(a)(b)(lambda _: a)(lambda _: f(MINUS(a)(b))(b))
REMAINDER = lambda a: lambda b: Z(REM)(a)(b)


# Recursive multiplication
# This is multiplication as repeated addition

m = lambda f: lambda a: lambda b: IF(IS_ZERO)(b)(lambda _: ZERO)(lambda _: ADD(a)(f(a)(PRED(b))))
RMULT = lambda a: lambda b: Z(m)(a)(b)


# Euclids gcd algorithm
GCD_STUB = lambda f: lambda a: lambda b: IF(IS_ZERO(b))(lambda _: a)(lambda _: f(b)(REMAINDER(a)(b)))
GCD = lambda a: lambda b: Z(GCD_STUB)(a)(b)


assert FACTORIAL(SUCC(FOUR))(lambda x: x+1)(0) == 120
assert FIBONACCI(FOUR)(lambda x: x+1)(0) == 5
assert DIVIDE(MULT(FOUR)(TWO))(THREE)(lambda x: x+1)(0) == 2
assert REMAINDER(MULT(FOUR)(TWO))(THREE)(lambda x: x+1)(0) == 2
assert REMAINDER(TEN)(FOUR)(lambda x: x+1)(0) == 2


'''
Lists
Generated as pairs of pairs
NIL is the empty list
IS_NIL tests for the empty list
'''

NIL = PAIR(TRUE)(TRUE)
IS_NIL = lambda l: l(FST)
CONS = lambda h: lambda t: PAIR(FALSE)(PAIR(h)(t))

HEAD = lambda l: IF(NOT(IS_NIL(l)))(lambda _: l(SND)(FST))(lambda _: NIL)
TAIL = lambda l: IF(NOT(IS_NIL(l)))(lambda _: l(SND)(SND))(lambda _: NIL)

MAP_STUB = lambda f: lambda g: lambda l: IF(IS_NIL(l))(lambda _: l)(lambda _: CONS((g)(HEAD(l)))(f(g)(TAIL(l))))
MAP = lambda g: lambda l: Z(MAP_STUB)(g)(l)

APPEND_STUB = lambda f: lambda l: lambda e: IF(IS_NIL(l))(lambda _: CONS(e)(l))(lambda _: CONS(HEAD(l))(f(TAIL(l))(e)))
APPEND = lambda l: lambda e: Z(APPEND_STUB)(l)(e)

LEN_STUB = lambda f: lambda c: lambda l: IF(IS_NIL(l))(lambda _: c)(lambda _: f(SUCC(c))(TAIL(l)))
LEN = lambda l: Z(LEN_STUB)(ZERO)(l)

LAST_STUB = lambda f: lambda l: IF(IS_NIL(TAIL(l)))(lambda _: HEAD(l))(lambda _: f(TAIL(l)))
LAST  = lambda l: Z(LAST_STUB)(l)

REVERSE_STUB = lambda f: lambda l: IF(IS_NIL(l))(lambda _: l)(lambda _: APPEND(f(TAIL(l)))(HEAD(l)))
REVERSE = lambda l: Z(REVERSE_STUB)(l)

FOLDR_STUB = lambda f: lambda g: lambda c: lambda l: IF(IS_NIL(l))(lambda _: c)(lambda _: g(HEAD(l))(f(g)(c)(TAIL(l))))
FOLDR = lambda g: lambda c: lambda l: Z(FOLDR_STUB)(g)(c)(l)

FILTER_STUB = lambda f: lambda p: lambda l: IF(IS_NIL(l))(lambda _: l)(lambda _: IF(p(HEAD(l)))(lambda _: CONS(HEAD(l))(f(p)(TAIL(l))))(lambda _: f(p)(TAIL(l))))
FILTER = lambda p: lambda l: Z(FILTER_STUB)(p)(l)


l = CONS(ONE)(CONS(TWO)(CONS(THREE)(CONS(FOUR)(NIL))))
k = MAP(MULT(TEN))(l)

assert HEAD(l)(lambda x: x+1)(0) == 1
assert HEAD(TAIL(l))(lambda x: x+1)(0) == 2
assert HEAD(TAIL(TAIL(k)))(lambda x: x+1)(0) == 30
assert HEAD(TAIL(TAIL(TAIL(k))))(lambda x: x+1)(0) == 40
assert LEN(l)(lambda x: x+1)(0) == 4
assert LEN(APPEND(l)(FIVE))(lambda x: x+1)(0) == 5
assert LAST(APPEND(l)(FIVE))(lambda x: x+1)(0) == 5
assert HEAD(REVERSE(l))(lambda x: x+1)(0) == 4