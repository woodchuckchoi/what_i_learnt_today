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
