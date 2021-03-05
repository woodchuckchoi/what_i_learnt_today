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

# Sidecar Pattern For Micro-services
한 Host의 여러 application이 HTTP(Loopback)를 통해서 inter-process communication하는 Service Design\
thick lib과 reference를 decouple하며, 각 application(micro-service)는 독립적으로 사용, refactor할 수 있다. 각 service에 알맞는 언어를 사용하여 Polyglot하다는 장점이 있다.\
HTTP를 사용하여 통신하므로 Latency가 존재하며, Service 구성에 complexity가 존재한다는 단점이 있다.

---


# Micro Service Architecture
Monolithic Desgin에서 개발과 관리의 어려움(매번 다른 팀이 배포를 할 때마다 코드에서 에러가 발생한다면?)을 이유로 MicroService로 이동하는게 n년 전~현재의 trend이다.\
MicroService를 적용하는데 그 크기는 회사, 팀마다 상이하다.\
예를 들어 모 미디어 기업은 추천 서비스, 검색 서비스 등 서비스를 기능별로 나누었음에도 ~10개의 마이크로 서비스를 가진다.\
반면 Uber는 2,000개가 훨씬 넘는 마이크로 서비스(어떤 마이크로 서비스는 단순히 메세지 큐에 데이터를 전달하는 역할을 한다)를 배포/운영하는 것으로 알려져 있다.\
또한 마이크로 서비스를 어떻게 나눌 것인가 역시 정해야 할 문제다.\
가장 일반적인 예는 인증 기능을 각 마이크로 서비스가 모듈로 탑재할지, 아니면 모든 요청이 인증 서버라는 마이크로 서비스를 거쳐 각 도메인에 맞는 마이크로 서비스에 전달될지이다.\
이런 문제를 해결하고 MSA가 안정기에 접어들었다고 하더라도 다시 새로운 패러다임의 도입은 불가피한 것으로 보인다.\
앞서 말한 Uber는 2,000개가 넘는 마이크로 서비스를 운영하며 수 천개의 엔드포인트 관리의 어려움, 마이크로 서비스 사이의 디펜던시 문제 등 MSA를 도입함으로써 생기는 문제를 DOMA (Doman Oriented MicroService Architecture)라는 패러다임으로 해결하고 있다고 한다.\
각 마이크로 서비스를 도메인으로 분류하고 엔드포인트를 도메인 레벨에서 관리한다.\
도메인은 다시 레이어라는 디펜던시 관리를 위한 추상적인 개념으로 분류한다.\
Uber 기술 블로그에서 한 기사 밖에 읽지 못했지만 더 알아볼만한 주제인 것 같다.


마이크로 서비스는 Network를 통해서 RPC 형태로 구성되지만, 네트워크 레이턴시의 대부분 DB에서 발생하는 보틀넥이므로 크게 상관할 일은 아니다.(Network Bandwidth는 대부분 CSP에서 10GB~ 수준이므로)\
오히려 신경쓸 부분은 Synchronous하게 진행되는 서버 / 로직이 있다면 각 마이크로 서비스에 Chain Reaction이 발생해서 느려질 수 있다는 부분이다.\
따라서 시간이 소요되는 부분, 요청이 전달되는 부분은 Async하게 메세지 브로커를 사용하거나, concurrent한 흐름을 만드는 것이 중요하다.\
여기에서 MicroService Architecture에 Go가 효율적임을 알 수 있다.\
Go HTTP 통신의 베이스가 되는 net/http 패키지는 Google에서 서버로 사용할만큼 퍼포먼스가 뛰어날 뿐만 아니라, 기본적으로 Request를 goroutine에서 처리해서 default로 async하다.

+ 왜 RESTful이 아닌 RPC를 사용하는가?
마이크로 서비스를 도입하면서 엔드포인트가 많아지는 것은 어쩔 수 없는 결과이다.\
Local Procedure Call이 아니니까.\
RPC를 사용하면 상대적으로 간단한 인터페이스(GET과 POST만 사용, payload는 body에 포함 등)를 제공한다. 하지만 RESTful은 단순히 엔드포인트가 많아짐을 넘어서 헤더와 리소스에 대한 정의까지 필요하다.\
따라서 많은 MSA는 REST가 아닌 RPC 기반으로 통신한다.

---

# NginX MicroServices 1
MicroService에서 App등 Front로부터 direct access가 들어오는 경우에는 API Gateway를 사용한다.\
API Gateway는 load balancing, caching, access control, monitoring 등을 담당하며, AWS API Gateway 혹은 NginX를 사용해서 implement한다.\
Loose Coupling을 통해서 MSA의 효과를 극대화하기 위해서 각 MicroService가 DB를 따로 가지는 것이 일반적이다.\
어쩔 수 없이 DB간에 overlapping되는 부분이 있고 Consistency를 위해서 더 implement할 게 많지만(eg. Redis를 application과 db 사이에 두고 여러 DB를 concurrent하게 update), 이로 인해 얻는 퍼포먼스, 구조 상의 이득이 일반적으로 더 크다.

MSA은 기본적으로 Distributed System이다. Concurrency는 물론, Durability 등 monolithic에서는 신경쓰지 않았던 많은 부분에 대비가 되어있어야 한다.\
또한 DB분리를 통해서 Eventual Consistency를 피할 수 없게 된다. 이에 대한 대비 역시 필요하다.\
MSA의 배포는 MSA에서 가장 복잡한 부분 중 하나다.  Service Discovery, Scaling 등에 대한 고민이 필요하며, 일반적으로 K8S와 같은 Clustering Solution을 사용하여 구현한다.

---

# NginX MicroServices 2
MSA에서 Front가 MicroService와 통신하는데 사용할 수 있는 방법은 아래와 같다.

* Direct Communication
Front가 MicroService들과 직접 통신한다. 각각의 MicroService는 자신의 public endpoint를 가지게되며, 이 public endpoint는 load balancer를 가리켜서 scaling을 할 수 있도록 한다.\
이 방법의 문제점은 Client가 필요한만큼 Public Network를 통해서 통신을 해야한다는 점이다.\
예를 들어 어떤 페이지를 로드하는데 필요한 MS가 10개라면 그만큼의 통신이 Public Network를 통해서 이루어져야한다. 이러한 통신을 public network를 통해서 연결한다면 (특히 mobile환경인 경우에) performance 저하뿐만 아니라 front 코드의 복잡함도 문제가 된다.\
또한 MSA에 주로 사용되는 RPC, AMQP와 같은 protocol을 사용할 시 browser, firewall, mobile과 관련해서 문제가 생길 수 있다.\
Front와 Back이 coupling되어 있으므로 Back의 기능이 수정될 때, Front 역시 수정이 필요해지는 것 역시 문제점이다.

* API Gateway
위의 Direct Communication의 문제점을 해결하기 위해서 API Gateway를 사용한다.\
API Gateway는 시스템의 entry point역할을 하며, oop의 Facade pattern과 같은 역할을 한다.\
또한 Authentication, Monitoring, Load Balancing, Caching 등 기존 Server의 역할을 모두 지원한다.\
API Gateway는 보통 Client로부터 Request를 받아서 여러 Micro Service에 요청을 전달하고 이 결과를 모아서 다시 Client에게 전달한다. 이 과정에서 Protocol을 translate하는 역할도 수행한다.

```
예를 들어 /productdetails?productid=123 이라는 API Gateway의 entry point가 있다면 API Gateway는 내부적으로 아래와 같은 Request를 보내고 있을 수도 있다.

/productdescription?productid=123
/productimages?productid=123
/reviews?productid=123
/recommendations?productid=123
...

위의 Micro Service로부터 받은 응답을 모아서 다시 사용자에게 전달하는 역할을 한다. 평균적으로 API Gateway의 한 Endpoint는 6~7개의 Micro Service에 결과를 요청한다.
```

API Gateway를 사용하면 Encapsulating을 통해서 Client와 Server 사이의 rount trip 횟수를 줄일 수 있으며 Front의 코드가 간단해진다.\
반면 API Gateway를 Highly Available하게 설정하고, Micro Service의 개발에 맞춰 API Gateway를 수정하는 과정에 대해 최적화를 해야한다. 그렇지 않으면 API Gateway가 서비스 개발의 bottleneck이 될 것이다.

API Gateway를 사용하기 위해서는 Micro Service로 보내지는 Request를 Concurrent하게 처리하고, 만약 Dependency가 있을경우 이에 순서를 맞추는 것이 중요하다.\
Micro Service의 위치가 계속해서 바뀌는 Cloud 환경에 대비하기 위한 Service Discovery가 필수적이며, Partial Failure에 대비한 개발 역시 필요하다.

---

# NginX MicroService 3
Monolithic과는 다르게 서비스가 분리된 Process 형태를 띄고 있는 MSA이므로, Service간 communication은 IPC(inter-process communication) 방식으로 이루어진다.\
Service간의 interaction은 아래와 같이 분류해서 생각할 수 있다.

1. First Dimension
    1. One-to-one - 하나의 Client Request는 하나의 Service Instance에서 처리된다.
    2. One-to-many - 각 Client Request는 여러 Service Instances에서 처리된다.
2. Second Dimension
    1. Synchronous - Client는 Service를 Synchronous하게 호출한다.
    2. Asynchronous - Client는 Service를 호출하고 block하지 않는다.

위의 분류는 아래와 같이 설명된다.
```
There are the following kinds of one‑to‑one interactions:

Request/response – A client makes a request to a service and waits for a response. The client expects the response to arrive in a timely fashion. In a thread‑based application, the thread that makes the request might even block while waiting.
Notification (a.k.a. a one‑way request) – A client sends a request to a service but no reply is expected or sent.
Request/async response – A client sends a request to a service, which replies asynchronously. The client does not block while waiting and is designed with the assumption that the response might not arrive for a while.
There are the following kinds of one‑to‑many interactions:

Publish/subscribe – A client publishes a notification message, which is consumed by zero or more interested services.
Publish/async responses – A client publishes a request message, and then waits a certain amount of time for responses from interested services.
```

Client와 Server가 분리된 개발 환경에서 위의 조건에 부합하는 API를 디자인하기 위해서 API-first approach가 사용된다.\
Interface Definition(protobuf와 같은)를 먼저 작성한 후, Client 개발자와 함께 리뷰한다. 모든 리뷰가 끝나면 실제 개발에 착수한다.\
Interface Definition을 정하는 것은 어떤 IPC mechanism을 사용하는가에 따라 달라진다.\
Messaging을 사용할 경우, API는 message channel과 message type이 될 것이고, HTTP를 사용한다면 URI, request/response format이 될 것이다.

Monolithic Pattern의 경우 API를 수정하고 이에 관련된 code를 update하는 것은 어렵지 않다.\
하지만 MSA의 경우 API 수정에 따른 기타 코드 수정을 한번에 할 수 없는 경우가 대부분이므로 backward-compatibility를 생각하며 개발 사항을 배포해야한다.\
사용하지 않는 resp의 field에는 default value를 사용하고, client도 쓰지 않는 field는 무시하는 방향으로 개발한다.\
backward-incompatible한 수정이 필요하다면, URL에 version을 명시하고 구버젼과 새로운 버젼을 한 Service에서 혹은 다른 Instance에서 동시에 동작하게 하는 방식을 사용한다.

Partial Failure에 대비하는 durability에 대한 고려 역시 필요하다. Netflix는 durability에 대한 문제 해결을 아래와 같이 정의한다.
```
Network timeouts – Never block indefinitely and always use timeouts when waiting for a response. Using timeouts ensures that resources are never tied up indefinitely.

Limiting the number of outstanding requests – Impose an upper bound on the number of outstanding requests that a client can have with a particular service. If the limit has been reached, it is probably pointless to make additional requests, and those attempts need to fail immediately.

Circuit breaker pattern – Track the number of successful and failed requests. If the error rate exceeds a configured threshold, trip the circuit breaker so that further attempts fail immediately. If a large number of requests are failing, that suggests the service is unavailable and that sending requests is pointless. After a timeout period, the client should try again and, if successful, close the circuit breaker.

Provide fallbacks – Perform fallback logic when a request fails. For example, return cached data or a default value such as empty set of recommendations.
```

이와 같은 IPC을 HTTP에서 하는 경우가 많다. HTTP를 사용하면 얻을 수 있는 장점은 아래와 같다.

* HTTP is simple and familiar.
* You can test an HTTP API from within a browser using an extension such as Postman or from the command line using curl (assuming JSON or some other text format is used).
* It directly supports request/response‑style communication.
* HTTP is, of course, firewall‑friendly.
* It doesn’t require an intermediate broker, which simplifies the system’s architecture.

단점은 아래와 같다.

* It only directly supports the request/response style of interaction. You can use HTTP for notifications but the server must always send an HTTP response.
* Because the client and service communicate directly (without an intermediary to buffer messages), they must both be running for the duration of the exchange.
* The client must know the location (i.e., the URL) of each service instance. As described in the previous article about the API Gateway, this is a non‑trivial problem in a modern application. Clients must use a service discovery mechanism to locate service instances.

주로 사용되는 포맷인 HTTP(REST)를 대체할 대안으로는 RPC(주로 Thrift를 이용)가 있으며 어떠한 포맷을 사용하느냐에 따라 Message의 format에 대한 선택도 달라진다.

---

# NginX MicroService 4
다른 Process(혹은 instance)에 존재하는 Service와 RPC(REST도 넓은 의미의 RPC에 속한다)로 소통하기 위해서는 네트워크 상의 주소(주로 ip와 port)를 알아야한다. Cloud 환경에서는 과거와 다르게 Instance가 autoscaling, fail-over 등의 이유로 유동적으로 바뀌기 때문에 service를 주소가 아닌 다른 방법으로 인식하는 기능이 필요하다.\
위의 기능은 client-side discovery와 server-side discovery 두 가지 방식으로 구현 가능하다.

1. Client-side Discovery
Client가 service discovery와 load balancing 전부를 담당하는 방식으로 Client는 service registry(현재 사용 가능한 service 서버 목록 database)에 query를 보내서 instance를 정한 후, 해당 instance에 요청을 전달한다.\
Service Instance를 refresh하는 데에는 일반적으로 heatbeat mechanism(일정 시간마다 ping을 보내서 service status == alive 를 확인하는 방식)을 사용한다.\
Client-side Discovery는 구조가 간단하고 service registry를 제외하면 dynamically modified되는 부분이 없다. 또한 Client가 service에 대한 정보를 가지게 되므로, 각 service에 맞는 load balance 방식을 적용할 수 있다. 하지만 Client와 Service Registry가 coupling되어 있으므로 모든 client에서 service registry와 관련된 logic을 구현해야한다.

2. Server-side Discovery
Client는 load balancer에 query를 보내고 load balancer가 service registry와 통신을 통해서 Service Discovery를 구현한 방식으로 NginX, AWS ELB, K8S의 default service discovery logic이 여기 속한다.\
Client로부터 Service Discovery logic이 분리되어 있으므로 client에서 구현이 간단해지며, Server-side Discovery를 제공하는 tool을 바로 사용할 수 있다. 반면 Load balancer와 같은 서비스를 개발 환경이 제공해주지 않는다면 스스로 구현해야한다는 단점이 있다.

Service Registry는 Service Discovery Feature의 중심으로 highly available, up-to-date한 database이다.

---

# NginX MicroService 5
MSA에서 각 서비스는 각자의 schema를 가진, 혹은 각 서비에에 맞는 종류의 DB를 가지는 것이 일반적이다.\
이와 같은 환경에서 data consistency를 유지하기 위해서 event-driven architecture를 구성한다.

Event-driven Architecture는 아래와 같은 Process를 거쳐 동작한다.

* BASE Model
1. A 서비스에 Request가 도착하면 A DB를 수정(Pending)하고 Message Broker를 통해서 연관된 B 서비스에도 Request를 전달한다.
2. B 서비스는 B DB를 수정하고 Message Broker를 통해서 A에게 OK Status를 전달한다.
3. OK를 전달받은 A 서비스는 1에서 수정한 DB Entry를 OK상태로 전환한다.

Event-driven 방식에 따라서 아래와 같은 구조를 사용하기도 한다.
1. Client에서 A 서비스와 B 서비스에 Request를 보낸다.
2. A와 B 서비스는 OK Status를 Message Broker에 전달한다.
3. Message Broker에 일치하는 A, B의 OK Status를 발견하면 Updater 서비스는 DB를 update한다.
4. Update된 DB를 Viewer 서비스로 확인한다.

위의 경우 DB에서 다시 Join을 하는 경우 Consistency에 대한 문제가 재발생하므로 Document DB(MongoDB)를 사용하여 Order가 생겼을 때 기존 Document에 append하는 방식을 사용하는 경우가 많다.\
Event-driven Data를 구성하면 다수의 DB 사이에 Transaction과 eventual consistency를 구현할 수 있지만, 단일 DB를 사용할 때보다 복잡한 구성이 필요하다.

Event Driven에서 Atomicity를 구현하기 위해서 Event Table을 두는 경우도 고려해야한다.\
A 서비스는 A DB를 업데이트하면서 이와 동시에 Event table에 어떤 서비스에서 어떤 일을 해야하는지를 Tasnaction으로 처리한다.\
Event table을 query하는 event publisher는 해당 event를 message broker에 전달한다.\
MSA에서 atomicity를 구현할 수 있지만, 개발 단계에서 신경써야할 부분이 많아지며, NoSQL을 사용할 경우 transaction과 query 지원이 RDB보다 상대적으로 부족할 수 있다는 단점도 있다.

위의 방식과 비슷하면서도 다른 Log Mining 방식도 있다.\
A 서비스가 A DB를 update할 떄 발생하는 log를 log miner Service가 message broker에 전달하는 방식으로 DynamoDB가 이를 사용한다.\
event의 atomicity를 구현하며, application의 business logic과 atomicity 구현과 같은 technicalities를 분리할 수 있지만, DB의 종류 혹은 DB 버젼 사이에도 log가 다르기 때문에 이에 대한 확인이 필요하다는 점이다.

Event Sourcing을 사용하는 방법도 있다.\
Event Sourcing은 DB에 Entity의 state를 저장하지 않고 event를 저장하고 다른 서비스들이 이 event를 subscribe해서 상태를 다시 추적하는 방법으로, Event는 단일 객체이므로 atomicity는 자연스럽게 구현된다.\
Event Sourcing을 통해서 MSA의 data consistency를 해결할 수 있으며 "OOP-RDB의 mismatch로 발생하는 문제"도 피할 수 있기 때문에 monolithic에서 msa로 변환을 쉽게 할 수 있다는 장점이 있다.\
하지만 기존의 스타일과 확연히 차이가 있기때문에 learning curve가 높은 편이며, eventual consistent를 피할 수 없다는 단점이 있다.

---

# NginX MicroService 6
MSA의 배포 역시 Monolithic과 큰 차이가 있다.\
Monolithic의 배포와 같은 방식으로 각 서버마다 동작에 필요한 서비스를 넣어서 배포할 수도 있다.\
이 방식은 배포가 빠르고, resource를 효과적으로 사용할 수 있으며, service startup이 빠르다는 장점이 있지만, service 사이의 coupling, service간의 resource 제한 불가, 운영 부서에서 각 service가 어떻게 연결되는지 알아야 한다는 단점 또한 있다.

각 Host에 service를 가상화해서 배포하는 방식의 경우 위의 monolithic 배포와 정반대의 장점과 단점을 지닌다. 각 Service는 loose coupling되어 있으며, resource를 제한 가능, Scaling이 자유롭다는 장점이 있는 반면 상대적으로 긴 startup time과 learning curve가 단점이다.

Serverless(AWS Lambda) 배포 방식의 경우 long-running application에는 맞지 않는 방식으로 request가 도착하면 이에 맞춰 instance가 동작한다. Request는 300초 이내에 응답되어야하며, 각 request는 다른 instance에서 동작할 수도 있기 때문에 (cache가 존재함에도 불구하고) state를 저장하는 application에는 적합하지 않다.

---

# NginX MicroService 7
Monolithic Legacy code를 MSA로 refactor하는 경우 처음부터 MSA를 새로 시작하는 Big Bang 방식은 지양한다.\
대신 monolithic을 incrementally rewrite하는 방식을 지향해야한다. 새로운 기능을 구성하는 Micro Service를 기존 Legacy와 함께 운영하여 Monolithic이 점차적으로 사라지거나, 하나의 micro service로 변화하도록 한다.

Incremental Refactoring은 아래와 같은 방식으로 구현할 수 있다.

1. Stop Digging - Monolithic code에 기능을 추가하는 것을 중지하고 해당 기능을 담당할 micro service를 구축한다. 일반적으로 API Gateway를 통해서 Monolithic과 Micro Serivce가 같은 endpoint를 사용하도록 하며, monolithic의 코드나 데이터를 사용하기위해서 glue code를 구성할 수 있다.
2. Split Frontend and Backend - (Self-explanatory)
3. Extract Services - Monolithic에서 Service를 분리하여 Micro Service를 만든다. Micro Service가 만들어짐에 따라서 Monolithic의 크기는 줄어든다. Micro Service를 충분히 분리했다면 Monolithic 역시 Micro Service가 되어있거나, 사라졌을 것이다. 

가장 수정이 자주되는 module을 먼저 분리해서 micro service로 만듦으로써 overhead를 줄인다. 또 resource를 가장 많이 차지하는 module을 분리함으로써 효율적인 배포 환경을 구성한다. 분리되는 모듈의 dependency는 REST API 등 interface를 구성해서 

```
Monolithic [X -> Y -> Z]

Monolithic [X] -> MS [Y] -> Monolithic [Z]
```
와 같이 구성한다.

---

# AWS API Gateway and Lambda
API Gateway가 Service의 Entry Point 역할을 한다는 정의에서 내가 가장 알고 싶었던 점은 다중 Request를 보내고 이것을 aggregate하는 MSA에서는 API Gateway를 어떻게 사용하는가였다.\
정답은 "aggregate하는 integrate layer(주로 lambda)를 둔다"이다.\
API Gateway는 다중 request 전송 후 이를 모아서 모델링해서 전달하는 역할을 하지 않는다.(그런 서비스도 있을 수 있겠지만)\
이러한 역할은 사실상 동시성, 모델링 등 프로그래밍 분야기 때문에 가볍게 사용할 수 있는 Lambda와 같은 serverless에 넘기고 API Gateway는 authorisation, monitoring, routing의 역할을 담당한다.\
그렇다면 사실 NginX에서 모두 할 수 있는 일이고, 거기에 AWS API Gateway는 load balancer도 따로 설정해야되므로 NginX의 압승이 아닌가?하는 생각도 들었지만 SaaS로 인프라, 네트워크같은 부분을 신경쓰지 않아도 된다는 면은 AWS API Gateway의 장점이라고 본다.\
현재 서비스에 Integration Layer로 Lambda가 상당히 많아질 것이라고 예상하는데 다행히 Terraform 도입을 얼마 전 시작해서 API Gateway와 Lambda 연결을 Terraform으로 관리한다면 그나마 좀 관리가 수월할 것 같다.

---

# MSA - Production-Ready Microservices
확장성, 효율성, 개발 속도, 새로운 스택 적용에 대한 어려움을 이유로 monolith -> MSA로 변경한다.\
하지만 MSA 자체적으로 가진 문제도 있다.\
확장 가능한 MSA를 구성하기 위해서는 인프라 레벨부터 수정해야 하는 경우가 많다.

작업을 효율적으로 처리하려면 앱은 동시성과 파티셔닝을 지원해야 한다.\
각각의 작업을 더 작게 분할하고, 여러 작업을 동시에 수행하는 것이 기본적인 필요조건이지만, 모든 서버에 전개하고, 어떤 일이든 처리해야하는 monolith는 이 두가지를 지원하기 힘들다.(하드웨어 scaling이 유일한 방법인 경우가 많다.)

위와 같이 Monolith -> MSA 패턴은 아마존, 우버, 넷플릭스 등 많은 회사에서 공통적으로 수행된다.\
MSA를 도입함으로써 확장성 뿐만 아니라, 개발 생산성, 속도 향상, 테스트 효율성 향상, 신기술 적용 용이 등의 이점이 함께 딸려온다.\

---

# The Clean Architecture
The flow comes from the outer layers, and goes into the inner layers.
Inner layers have no information (dependency) on the outer layers.
```
IN
								Entities
										^
										|
								Use Cases
										^
										|
					Controllers (Gateways, Presenters)
										^
										|
	External Interfaces (DB, Devices, Web, UI)
OUT


Presenter -> Use Case Output Port
									^
									|
					   Use Case Interactor
									|
									v
Controller -> Use Case Input Port

Flow of control: Controller -> Use Case Interactor -> presenter

```

* Entities
- Represent your domain object
- Apply only logic that is applicable in general to the whole entity (e.g., validating the format of a hostname)
- Plain objects: no frameworks, no annotations

* Use Cases
- Represent your business action: it's what you can do with the application. Expect one use case for each business action
- Pure business logic, plain code (except maybe some utils libraries)
- The use case doesn't know who triggered it and how the results are going to be presented
- Throws business exceptions

* Interfaces / Adapters
- Retrieve and store data from and to a number of sources (database, network devices, file system, etc)
- Define interfaces for the data that they need in order to apply some logic. One or more data providers will implement the interface, but the use case doesn't know where the data is coming from
- Implement the interfaces defined by the use case
- There are ways to interact with the application, and typically involve a deliverymechanism (REST, GUI, etc)
- Trigger a use case and convert the result to the appropriate format for the delivery mechanism
- The controller for a MVC

* External Interfaces
- Use whatever framework is most appropriate (isolated)

```
src (lib)
├	entities							// Data object
├ external_interfaces		// Server and Endpoint 
├ interface (adaters)		// Controller
└	use_case							// Core Logic
```
