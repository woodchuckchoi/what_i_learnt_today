# MVC Pattern
소프트웨어를 개발하는데 사용되는 디자인 패턴 중 하나로,
* Model은 DB와 통신을 통해서 View를 Update한다.
* View는 User가 보는 화면에 DB의 Data를 렌더링한다.
* Controller는 User가 원하는 Data를 Model에 요청하고 이를 View에 전달한다.

# 5 Design Patterns Every Engineer Should Know
*From Jr. to Lead. == Framework Consumer to Framework Creator*

* Singleton
eg)Database Driver -> Multiple Customers\
한 클래스를 차지하는 인스턴스가 하나만 있는 디자인\
디자인이 간단하며, 사용이 편리하지만, Payload가 높을 때 단일 인스턴스에서 Bottle Neck이 발생한다.\

* Facade
Facade를 통해서 inner logic을 숨긴다. Compiler의 경우 내부에 수많은 기능이 있지만 제공하는 이를 외부에 제공하지 않는다. Interface가 간단해지고 접근성이 높아지지만, 가지고 있는 기능성을 추상화하는데서 가치를 잃을 수 있다. 또한 single usecase에 맞춰져서 over-simplified(충분히 generalised 되지 않는다) 될 수 있다.

* Bridge
많은 기능을 가진 Application에 use case에 일치하는 Bridge를 연결하여 사용자가 접근성이 더 높은 Bridge에 접근하게 한다. Bridge를 과하게 사용할 시, 개발해야할 양이 늘어난다. 새로운 Bridge는 필요할 때 개발하면 되기 때문에 나중에 개발한다.

* Strategy
많은 기능을 가진 Application를 strategy별로 분리한다. 각 Strategy의 default를 간단하게 설정하고, 필요에 따라 확장하지 않으면 over-complex하다.

* Observer(Pub/Sub)
Publisher와 Subscriber(s)의 loose coupling이 가능하다. 어디에나 사용할 수 있다. 하지만 Pub/Sub 모델이 복잡해지면 Event Loop이 복잡해져서 debug에 어려움이 있다.

---

# Uber's New Backend Architecture
모든 Process를 기능 단위로 분리했다.\
심지어 Message Queue에 Insert를 하는 Process도 분리시켜놨음\
이 경우 Message Queue를 변경해도 쉽게 교체가 가능하겠지만 Micro Service로 구축할지 Monolithic의 한 부분으로 구성할지는 Trade-off를 보고 결정해야 할 듯

Google, Uber처럼 Global Scale인 경우 최소한의 Error를 가지는 Atomic Clock을 사용해서 ACID를 유지한다.\
Time Zone에 따른 차이를 극복하는 것이 Global Scale Service가 필요한 점 (Unless 각 Region마다 각각의 Server를 구성)

---

# Streaming Service
왓챠같은 비디오 스트리밍 서비스는 (각각 다르지만) 어떻게 동작하는 것일까?\
Pay, Recommendation 등 다른 서비스도 중요하지만, Streaming 서비스가 중심이다. 다른 서비스와는 다르게 대용량 정보를 끊김없이 제공해야되기 때문에 아키텍쳐, 프로토콜이 일반적인 CRUD 서비스와는 차이가 있을 수 밖에 없다.\
예를 들어 Youtube는 UDP(HTTP3) 통신을 통해서 Byte 데이터를 전송받는다. 그렇게 전달받은 Byte 데이터를 Front가 렌더링하는 것으로 보인다.\
반면 왓챠는 HTTP2(TCP) 프로토콜로 동영상 데이터인 mp4를 AWS S3 -> Cloud Front로부터 전달받는다. 특이한 점은 각 Request의 URI가 같다는 것이다.\
계속 바뀌는 영상 데이터인데 엔드포인트는 같다? 그렇다면 S3 Static Serving에 계속해서 UUID의 URI에 실시간으로 영화를 잘라서 넣거나 미리 잘라놓은 영상을 계속 업데이트 한다는 뜻일까?\
Request Header에는 "range"라는 내 이론과 꽤나 잘 맞을 것 같은 Header도 있다.\
아무리 생각해도 실시간으로 영상을 처리하는 건 너무 overhead가 크기 때문에 Batch 작업으로 처리한 짧은 영상을 복붙하는 것 같은데, 복붙도 문제가 있다.\
S3에 복붙을 한다고해도 1. S3는 Strongly Consistent하지 않고 2. S3의 최대 속도가 수백 MB라도 실시간 스트리밍 서비스에는 느릴 수도 있다.\
그렇다면 나한테 보여지는 URI에는 보이지 않는 service가 URI, Header의 range를 조합해서 그 순간에 맞는 영상으로 forward해주는 서비스가 있다고 생각할 수 밖에 없다.\
endpoint URI를 숨김으로써 얻는 이득은 공격에 대한 방어일까? 하지만 해당 URI에 접속하면 (Broken) 영상이 보이는데;; 아키텍쳐가 어떤지는 모르지만 Auth와 관련해서 고칠 점이 있는건가

---

# Bloom Filter
만약 a라는 user가 있는지 확인하고 싶다면, was에 request를 보내고 was는 db에 select를 통해서 a가 있는지 확인 후 response를 보내야 한다.\
이 때 생기는 round trip을 최소한으로 처리하기 위해서 redis와 같은 메모리에 응답값을 저장한 후, 그 응답을 활용할 수 있다.\
하지만 이와 같은 문제를 막기 위한 solution, bloom filter를 사용할 수도 있다.

## Bloom Filter
Hashing 값을 통해서 DB에 값이 해당 Hashing 값을 가지는 이름이 이미 있는지를 알 수 있다? HOW?\
Cassandra도 내부적으로 Consistency를 체크하기 위해서 Bloom Filter를 사용한다.\
Application이 stateful해진다, memory intensive하다, redis를 사용하는 것과 큰 차이가 없다.\
Implementation에 따라 spec 차이가 있겠지만 지금 생각으로는 서비스 적용에 크게 이득이 없을 것이라고 예상됨

---

# Reddit Being Slow
New Reddit은 lazy evaluation하던 old reddit에서 모든 data를 다 load하는 웹앱으로 변경했다.\
대부분의 overload는 static data (video, image)가 차지했지만 불필요한 javascript 역시 적지 않은 용량을 차지한다.\
graphql을 사용하고 (아마도) 새로운, 더 낫다고 여겨지는 web framework를 적용했지만 performance boost와 new tech가 항상 같은 것은 아니다.

p.s. PNG의 animated version인 apng가 존재한다!

---

