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
