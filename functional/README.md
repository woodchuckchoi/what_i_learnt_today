# Functional Thinking
GC와 마찬가지로 점점 더 많은 기능을 Runtime이 담당하는 경우가 늘고 있다.\
이는 Human Mistake를 줄일 뿐만아니라, Runtime의 Optimisation이 성능 향상에도 도움이 되기 때문이다.\
객체지향에서 클래스와 여기에 속한 메소드(과정)를 선언하는데 반해 함수형에서는 내가 얻고자 하는 결과를 선언(declarative)하고 Runtime에게 과정을 맡긴다.(pure functional language가 아니라면 필요한 몇몇 class를 선언하는 것 역시 포함될 것이다)\
이에 따라 더 간단하고, side-effect가 없는 (복잡성을 줄일 수 있는) 코드를 짤 수 있게된다.\
간단한 예시는 아래와 같다.

객체지향&절차형
```
# in python
class Number:
    def __init__(self, num):
        self._num = num

    def get_divisor(self):
        ret = []
        for num in range(1, math.sqrt(self._num)+1):
            if self._num % num == 0:
                ret.append(num)
                ret.append(self._num//num)
        return ret

    def checkType(self):
        divs = self.get_divisor()
        if sum(divs) - self._num == self._num:
            return 1
        ...
```

함수형
```
# in elixir
def checkType(num):
    right = :math.sqrt num
    |> round

    sum = 1..right
    |> Enum.filter(fn x -> rem(num, x) == 0)
    |> Enum.map(fn x -> x + div(num, x))
    |> Enum.sum

    cond sum - num do
        num ->
            1
```

위의 예시와 같이 filter, map, reduce 등의 runtime에서 지원하는 기능을 사용하여 어떤 대상이 필요한지 declarative하게 선언하기 때문에 가독성, 개발 속도에서 강점이 있다.

---

# Functional Concepts

```

a is a value

put it in a context
Maybe a

Now when you apply a function to this value, you'll get different results depending on the context.

The Maybe data type defines two related contexts:
	data Maybe a = Nothing | Just a (either Nothing or Just a data type)

When a value is wrapped in a context, you can't apply a normal function to it
```

* Functor
This is where fmap comes in.
fmap knows how to apply functions to values that are wrapped in a context.

```
Suppose you want to apply +3 to Just 2.
> fmap(+3) (Just 2)
Just 5
```

Functor is a typeclass.
To make a data type f a functor, that data type needs to define how fmap will work with it.
```
class Functor f where
	fmap:: (a->b) -> fa -> fb
```

A functor is any data type that defines how fmap applies to it.
```
fmap:: (a->b) -> fa -> fb
1. fmap takes a function (arrow)
2. and a functor fa (like Just 2)
3. and returns a new functor (like Just 5)
```

Above, fmap works because Maybe is a Functor. It specifies how fmap applies to Just and Nothing:
```
instance Functor Maybe where
	fmap func (Just val) = Just (func val)
	fmap func Nothing = Nothing
```
Lists are functors too.
```
instance Functor [] where
	fmap = map
```

when apply a function to another function
```
> let foo = fmap (+3) (+2)
> foo 10
15
```
the result is another function.

so functions are functors too.

* Applicatives
Applicatives are "one-step-further" of functor.
Even functions can be wrapped in a context, and applicatives know how to apply wrapped functions to wrapped values.
```
Just (+3) <*> Just 2 == Just 5

but, also, something interesting can happen.

[(*2), (+3)] <*> [1,2,3]
[2,4,6,4,5,6]
```

```
> (+) <$> (Just 5)
Just (+5)
> Just (+5) <*> (Just 3)
Just 8

> (*) <$> Just 5 <*> Just 3
Just 15

```

* Monads
Monads add a new twist.
Functors apply a function to a wrapped value.
Applicatives apply a wrapped function to a wrapped value.
Monads apply a function that returns a wrapped value to a wrapped value.

Suppose half is a function that only works on even numbers
```
half x = if even x
					then Just (x `div` 2)
					else Nothing

half 3 = Nothing
half Just 3 // ERROR!

BUT

> Just 3 >>= half
Nothing
> JUst 4 >>= half
Just 2
> Nothing >>= half
Nothing
```

Monad is another typeclass.
```
class Monad m where
	(>>=) :: ma -> (a -> mb) -> mb

1. >>= takes a monad (like Just 3)
2. >>= then takes a function that returns a monad (like half)
3. and it returns a monad
```

so Maybe is a monad when
```
instance Monad Maybe where
	Nothing >>= func = Nothing
	Just val >>= func = func val
```

---

# Tail Recursion
A recursive function is tail recursive when recursive call is the last thing executed by the function.
The tail recursive functions considered better than non tail recursive functions as tail-recursion can be optimized by compiler. The idea used by compilers to optimize tail-recursive functions is simple, since the recursive call is the last statement, there is nothing left to do in the current function, so saving the current function’s stack frame is of no use. (Stack overhead nullified)

If you want to convert non-tail recursive function to tail recursive function, you'll probably have to add another parameter to store the result.

---

# Learn from Haskell 
1. Functions can be applied to their arguments one at a time, which is called currying.
```
average :: Float -> Float -> Float
average a b = (a + b) / 2.0

avgWith3 = average 3
avgWith3 5
>> 4.0
```

2. Infix and Prefix are interchangeable
```
(+) 1 4
>> 5
(*) 21 2
>> 42

2 `average` 3
>> 2.5
```

3. Overloading in Functional
```
(+) :: Int -> Int -> Int
(+) :: Float -> Float -> Float

// therefore

(+) :: a -> a -> a where a == Int | Float | any Num type class(set of types) // where ... == Num a
(+) :: Num a => a -> a -> a
(==) :: Eq a => a -> a -> Bool
show :: Show a => a -> String
```


---
