# Deadlock
프로세스의 집합이 더 이상 진행되지 못하고 영구적으로 블록된 상태이다.\
서로 다른 프로세스가 서로 충돌되는 자원을 요구할 때 발생한다.\
Deadlock(교착)이 생기는 조건은 다음과 같다.
* 상호 배제: 한 번에 한 프로세스만 어떠한 자원을 사용할 수 있다.
* 점유 대기: 이미 자원을 가지고 있는 프로세스가 다른 자원을 요청할 수 있다.
* 비선점: 프로세스에 의해 점유된 자원을 뺏을 수 없다.
* 환형 대기: 어떠한 자원을 점유한 프로세스가 해당 자원을 필요로 하는 다른 프로세스가 점유하고 있는 자원을 필요로 한다.

Deadlock의 해결 방안은
* 예방: 위의 4가지 Deadlock이 생기는 이유 중 하나를 시스템에서 허용하지 않는다.
	* 상호 배제는 데이터의 일관성을 위해서 예방할 수 없다.
	* 점유 대기는 어떤 프로세스가 필요로 하는 모든 리소스를 프로세스 시작 시에 한번에 요청하는 방식으로 해결할 수 있다. 다만 지금 사용할 리소스가 아닌 모든 리소스를 요청하므로, 해당 프로세스가 진행되는 동안 다른 프로세스가 자원을 사용할 수 없다는 단점이 있다.
	* 비선점은 어떤 프로세스가 필요로 하는 자원이 사용 중이라면 기존에 점유하던 자원을 반납하고 기다리거나, 다른 프로세스의 자원을 뺏는 방식으로 해결 할 수 있다.
	* 환형 대기는 자원에 프로세스 별 할당 순위를 주어 해결 가능하다.
* 회피: 자원 할당 단계에서 교착이 발생하지 않도록 동적으로 자원을 관리한다.
* 발견: Deadlock이 발견되었을 때, 프로세스를 중지시키고 Rollback하여 해결한다.

---

# Semaphore & Mutex
여러 프로세스나 스레드가 공유 자원에 접근하는 것을 제어하기 위한 수단이다.\
범용 Semaphore의 경우 Pool의 크기를 의미하는 Value가 양수이면 Resource를 할당하고, 음수이면 대기 Queue에 할당한다.\
이진 Semaphore는 뮤텍스와 흡사하게 Boolean Value라고 볼 수 있는 Lock을 설정했다, 해제했다 하며 자원을 관리한다. 차이는 Semaphore는 현재 Resource를 사용 중이지 않은 다른 프로세스가 Semaphore를 제어할 수 있지만, Mutex는 Resource를 가지고 Task를 수행중인 대상만이 Mutex를 제어할 수 있다는 점이다.

---

# Short Circuit Evaluation
C의 &와 &&처럼 같은 값이 나오는 연산일지라도 논리 연산자는 논리 연산에 최적화되어 AND 연산일 때, 앞의 값이 false라면 뒤의 값을 계산하지 않는다. 따라서 논리 연산이 필요한 곳에는 항상 논리 연산을 사용하자. 이것은 ||(OR)에도 마찬가지로 적용되어 앞의 값이 true라면 뒤의 값에 대한 연산을 하지 않는다. 따라서 조건문의 조건절에서 연산을 하도록 프로그래밍 할 때는 주의하자.

---

# Switch의 작동 방식
switch는 jump table을 생성하여, 이에 대한 Index를 기준으로 해당 조건문에 접근한다. 이 jump table은 case의 값에 따라 만들어 지게된다. case가 1~10의 값을 받는다면 jump table에는 0부터 9까지 값이 들어가서 주소 역할을 하는 것과 같다. (아마도 주소 역할을 하기 때문에 정수가 아닌 숫자가 들어갈 수도 없는 것 같다. 0X12FA1244.5 같은 주소는 없으니까..?)  그렇기 때문에 C에서는 switch에 변수를 사용할 수 없다. (미리 jump table이 만들어지는데, 값을 알 수 없는 변수가 들어가면 안되므로)\
if - else만큼 CMP를 수행하는 것과 다르게 jump table의 크기만 커질 뿐 O(1)의 성능으로 switch는 작동하기 때문에 case의 값의 크기가 작고, 정렬되어 있으며, 값 사이의 차이가 크지 않다면 효율적으로 switch를 사용할 수 있다.

---

# Framework VS Library
* Framework는 소프트웨어의 특정 문제를 해결하기 위해서 상호 협력하는 클래스와 인터페이스, 함수의 집합이다.
* Library는 활용 가능한 도구의 집합으로 사실상 Framework와 같은 것을 가르킨다고 볼 수 있다.

*Framework는 개발자가 Framework의 Flow에 필요한 Logic을 추가하며, Library는 도구로써 개발자가 원하는 기능을 만드는데 도움을 준다. Flow의 주체가 누구인가에 따라 구분할 수 있다*.

---

# OS Run Level
OS에서 시스템 관리를 편하게 하기 위해서 서비스의 실행을 각 단계별로 나눈 것이다.

* 0 Halt - 시스템 종료를 의미한다. Run Level을 0으로 변경하라는 명령을 내리면 시스템을 종료한다.
* 1 Single User Mode - 시스템 복원 모드라고도 하며, 관리자 권한의 쉘을 얻게된다. 주로 파일 시스템을 점검하거나 관리자 암호를 변경할 때 사용한다.
* 2 Multi-User Mode, without NFS - NFS(Network File System)을 지원하지 않는 다중 사용자 모드이다. 네트워크를 사용하지 않는 텍스트 유저 모드라고 할 수 있다.
* 3 Full Multi-User Mode - 일반적인 텍스트 인터페이스의 다중 사용자 모드이다.
* 4 기본적으로 사용되지 않는다. 임의로 정의하여 사용할 수 있다.
* 5 X11 - Level 3 Full Multi-User Mode와 같지만, GUI를 지원한다.
* 6 Reboot - 시스템 재부팅을 의미한다. Run Level을 6으로 변경하라는 명령을 내리면 시스템을 재부팅한다.

---

# Python
스크립트 언어는 기존에 존재하는 소프트웨어를 제어하기 위한 언어이다.\
예를 들어 JavaScript는 웹 브라우저 위에서 동작하며, 웹 브라우저의 행동을 제어한다.
Python은 OS를 제어하는 스크립트 언어이기도 하면서, 프로그램을 만들기도 하는 범용 프로그래밍 언어이다.\
또한 Python은 인터프리터 언어이다. 컴파일러 언어는 전체 소스코드를 읽은 후, 기계어로 컴파일하는 반면에, 인터프리터 언어는 한 줄 한 줄에 대해서 Intermediate 언어로 변환하여 Runtime이 해당 코드를 실행하게 한다. 일반적으로 컴파일 언어가 인터프리터 언어보다 코드의 실행 속도가 빠르다는 장점이 있지만, 컴파일에 시간이 걸린다는 단점도 있다.\
일반적으로 Python은 설치 시 CPython이라는 Python 환경으로 설치되지만, Pypy Implementation을 사용하여 성능 향상을 기대할 수 있다. Pypy는 JIT(Just-in-Time) 방식으로 동작하기 때문이다. JIT은 인터프리터가 Intermediate 언어로 바꾸던 방식을, 프로그램이 실행될 때 불러오는 Method를 JIT을 통해서 기계어로 컴파일하고, 이후에 해당 Method 요청이 들어오면 컴파일 된 Implementation을 사용하여 4~6배 정도 빠른 속도를 기대할 수 있다.\
데이터는 빠른 접근을 위해서 메모리에 저장된다. C 언어에서는 메모리를 할당하고, 해제하는 기능을 개발자가 직접하기도 하지만, Python과 같은 High-Level 언어에서는 메모리 관리를 Runtime이 스스로 한다.

*Runtime은 프로그램이 동작하는 동안 사용되는 라이브러리, 프레임워크, 플랫폼의 집합을 뜻한다.*

이것을 Garbage Collection이라고 한다. GC는 개발 생산성을 높여주며, 에러의 위험을 줄인다. GC가 동작하는데 메모리와 Computing Power가 필요하다는 단점이 있지만, Computing Power가 충분한 현대에는 크게 문제가 되지 않는다.\
Python에서 일반적으로 Garbage Collection에 사용되는 방법은 Reference Counting이다.\
변수의 Reference 횟수를 기억하고 있다가, 더 이상 등장하지 않으면 해당 메모리를 해제하는 것이다.

	a = 5 		# ref a = 1
	b = {'key': a} 	# ref a = 2

하지만 Reference Counting 시 Reference Cycle이 발생하기도 해서  General Garbage Collection 기법을 사용하기도 한다.

	a = TmpClass() 		# ref a = 1
	a.key = a		# ref a = 2
	del a			# ref a = 1, 지워진 a.key에 해당하는 a의 reference counting은 절대 0이 될 수 없다.

그렇기 때문에 어느 시점(Generation)에서 Reference의 갯수가 일정 수치(Threshold)를 넘는 순간 Garbage Collecting을 하는 General Garbage Collection을 병행한다.

GIL은 Python Global Interpreter Lock을 뜻한다. 한 번에 한 개의 스레드만 Python 인터프리터를 사용할 수 있도록 뮤텍스가 설정되어 있기 때문에, 멀티 스레드 환경에서 보틀넥이 발생한다.

---

# Process VS Thread
CPU에서 처리하는 일의 단위인 프로세스에는 한 개 ~ 여러 개의 스레드가 공존할 수 있다.\
프로세스와 스레드 모두 지금 코드가 진행되는 흐름에서 가지치기를 해서 독립적으로 움직이는 다른 코드의 흐름을 만든다는 공통점을 가지고 있지만, 일반적으로 프로세스를 만드는 것이 더욱 힘들고, 더 많은 리소스를 필요로 한다.\
하드웨어에서 스레드는 동일한 코어에서 다른 흐름을 만들지만, 프로세스는 다른 CPU 코어에서 동작하기 때문이다. (프로세스는 리소스를 복사하여 새로운 리소스를 사용한다.)\
그렇기 때문에 OS는 Kill, Stop 등의 Signal을 사용하여 프로세스를 제어한다.\
각 스레드는 Private한 메모리 공간(지역변수가 저장되는 Stack)과 공동으로 사용하는 메모리(그 외 전부)를 가진다.(하지만 여전히 포인터를 통해서 다른 스레드의 Private메모리에 접근할 수 있다.)\
Mutex와 같이 Thread-safe한 기능을 갖추지 않은 상태로 여러 스레드를 동작시키면, Racing Condition이 발생하여 예상하지 못한 결과값이 나올 수 있다.\
*변수에 어떤 연산을 하고 저장할 때, 다른 스레드가 해당 변수에 접근해서 연산을 무시하거나 예상하지 못한 결과를 가져올 수 있다*.
\
이를 막기위한 방법으로 한 번에 한 스레드만 일을 할 수 있도록 GIL을 설정한 것이다.\
Multi-Processing, 비동기성(Async)를 사용하여 동시성을 구현할 수 있다.

--- 

# Closure
클로저는 함수가 그 밖의 스코프에 접근하는 행위를 가리킨다. Python에서 Decorator와 같다.\
예를 들어 JS에서 for loop 안에 Timer를 설정해두고 for loop의 i값을 호출한다면, Timer가 실행되기전 모든 loop가 지나가서 마지막 i의 value만 출력이 될 것이다.\ 
하지만 closure를 이용하여 i를 변수로 받는 함수를 Timer가 호출하게 된다면 i를 그대로 출력할 수 있다.

	var obj = {};
	var items = ["click", "keypress"];
	for (var i = 0; i < items.length; i++) {
		(function() {
			obj["on" + items[i]] = function() {
				console.info("thanks for your " + items[i]);
			};
		})();
	}

위의 JS를 실행하면 obj.onclick()이나 obj.keypress()는 "thanks for your undefined"라는 값을 출력하게 된다.\
이는 for loop에서 i를 가장 안쪽의 스코프에 생성된 함수가 접근할 수 없기 때문이다. 그러므로 아래와 같이 변경하여, 함수가 만들어지는 환경에서 i에 접근할 수 있도록 해주면 함수가 정상적으로 작동한다.

	for (var i = 0; i < items.length; i++) {
		(function(i) {
			obj["on" + items[i] = function() {
				console.info("thanks for your " + items[i]);
			};
		})(i);
	}

클로저는 자기 자신에 대한 접근, 외부 함수의 변수에 대한 접근, 그리고 전역 변수에 대한 접근 3단계로 구분할 수 있다.\
위의 예시에서 외부 함수에서 선언된 변수가 아니며, 전역 변수도 아니기 때문에 접근이 불가능 했다.\
클로저를 통해 변수를 참조하는 동안에는 내부 변수가 차지하는 메모리를 GC가 회수하지 않기 때문에, 클로져의 사용이 끝나면 참조를 제거하는 편이 좋다.

---

# Concurrency
블럭 / 논블럭
* 블럭은 어떤 함수를 호출했을 때, 행위를 모두 끝마칠 때까지 기다렸다가 리턴하는 행위이다.
* 논블럭은 어떤 함수를 호출했을 때, 행위를 요청하고 결과가 나오지 않은 상황에서 바로 리턴하는 행위이다.

동기 / 비동기
* 동기는 A라는 행위와 B라는 행위가 순차적으로 인과관계가 있게 작동하는 것이다.
* 비동기는 A와 B라는 행위가 동시에 진행되는 것이다.
비동기의 가장 대표적인 사례는 AJAX 통신이다.\
AJAX 통신은 브라우저가 지원하는 XMLHTTPRequest를 이용하여 HTML Document 전체를 reload하지 않고 필요한 부분만 비동기적으로 처리하는 방식이다.\
JS라면 일반적으로 request.then().catch()와 같은 방식으로 callback을 설정하여 비동기적 함수 호출을 처리한다.\
이러한 비동기 처리에서 발생하는 문제 중 하나는 callback hell이다. Function이 종료되었을 때, 실행될 함수를 줄줄이 늘어놓아서 알아보기도, 개발하기도 힘든 상황을 뜻한다.\

이를 해결하기 위한 방법으로는
1. 함수의 패턴을 분리하여 A함수가 종료되면서 B함수를 실행시키도록 처리
2. JS의 Promise, Python의 Async Task처럼 아직 완료되지 않은 객체를 반환하는 방식으로 function.then() 내부의 callback function이 무한정 길어지는 callback hell을 해결할 수 있다.\

---

# Search Service
포탈들을 검색어 추천 서비스를 소켓이 아닌 HTTP/2 통신으로 진행한다.\
근래에 HTTPS를 사용하는 서비스는 HTTP/1.1에서 HTTP/2로 전환하려는 움직임이 있다.\
예를 들어 Naver와 Google. curl --http2 -I URI 를 해보면 헤더에 HTTP/2 OK가 명시되어 있는 것을 볼 수 있다.\
HTTP/2 환경은 Client의 Request에 대해 서버가 Response를 보내고 연결을 끊는 HTTP/1.1과 다르게 bi-directional한 다수의 Stream을 생성할 수 있다.\
HTTP/1.1은 단방향 통신을 여러 Connection을 열고, 소켓 통신을 연결해서 Server Push가 가능한 실시간 양방향 통신을 했지만, HTTP/2는 기본적으로 이런 기능들의 상위 호환을 제공하는 것이다.\
각 검색어는 한 글자 한 글자가 쳐질 때마다 Request를 보내고, 이에 대한 Request를 화면에 렌더링한다. (HTTP/2이므로 매번 연결을 생성, 해제하지 않아도 되서 Overhead가 적다.)\
검색 엔진의 경우 인터넷 상에서 데이터를 수집하는 Crawler 로봇을 사용하며, 이 로봇이 방문한 사이트는 인덱싱되어 DB에 저장된다.\
DB에 저장된 파일은 (아마도) 토픽을 추출하여, 해당 키워드가와 검색어가 얼마나 일치하는가를 각 검색 엔진의 알고리즘을 통해서 계산한다.\
\
*아마도 조건부 확률이니까 기본적으로 베이즈의 정리를 사용하지 않을까?*

	P(A|B) = P(B|A) * P(A) / P(B)
	몬티홀의 역설
	P(당첨|바꾼다) = P(바꾼다|당첨) * P(당첨) / P(바꾼다) 당첨이 되었는데 바꿔서 당첨이 되었을 확률은 A가 스포츠카일 때 B를 선택, C를 선택이므로 확률은 2/N(어떤 상수)이라 할 수 있다.
	P(당첨|안바꿈) = P(안바꿈|당첨) * P(당첨) / P(안바꿈) 당첨이 되었는데 안바꾸서 당첨이 되었을 확률은 A가 스포츠카이고 A를 선택했을 때 뿐이므로 확률은 1/N(어떤 상수)라고 할 수 있다. 따라서 바꾸는 편이 당첨될 확률이 2배 높다.

---

# HEAP
HEAP은 부모 노드가 항상 자식 노드보다 크거나 (Max Heap), 작은 (Min Heap) 데이터 구조이다.\
한 부모 노드가 두 자식 노드를 가지는 Binary Heap이 널리 사용된다.\
부모 노드의 Index가 n일 때, 자식 노드의 Index는 각각 2n+1, 2n+2이 되어 연산이 편하다는 장점도 있고.

---

# Hashmap
Hash 함수라는 함수를 통해서 어떠한 데이터를 Index화 하여 해당 Index의 데이터에 접근하는 데이터 구조이다.\
어떤 Data도 O(1)에 접근할 수 있다는 장점이 있지만, (Hash 함수에 정도가 다르긴 하지만) 언젠가 같은 Index를 만들 수도 있다는 단점도 있다.\
이를 막기위해서 가장 자주 사용되는 방법은 Hashmap의 Value를 Linked-List로 만들어서 한 Index에 여러 값을 저장할 수 있도록 하는 방식이다.\

---

# Memory Allocation
프로그램을 실행하면 프로그램은 RAM에 적재된다. 적재될 때는 코드 세그먼트와 데이터 세그먼트 두 부분으로 나뉘게 된다.\
메모리의 가장 낮은 주소(물리적으로 가장 낮은지는 알 수 없다, 운영체제에서 물리적인 메모리와 논리적인 메모리 주소를 Paging 기능을 통해서 매치하기 때문)에는 코드 세그먼트가 존재하며, 그 위에는 상수와 리터럴이 존재하는 Read-only data, 그 위에는 전역 변수와 Static 변수, 사용자 정의 영역인 힙 이 순서대로 위치하며, 지역변수가 위치하는 스택은 할당된 메모리의 가장 끝부분에서 주소가 낮아지는 방향으로 생성된다.\
사용자 정의 영역인 힙에는 Malloc과 같은 방식으로 사용자가 정의하는 메모리를 할당한다.

---

# Ducktyping
Python, Go 등에서는 어떠한 기능을 가지고 있는 Obj를 그 type으로 취급할 수 있다.\
예를 들어 Python에서는 type을 알 수 없지만, .append라는 기능이 있다면 그 기능을 사용하도록 할 수 있다.\
Go의 경우에는 Interface를 사용하여 어떠한 함수가 있는 Type에 대해 공통적으로 사용할 함수를 선언 할 수 있다.\
이처럼 Looks like a duck, sounds like a duck. Then it is a duck. 이라는 철학에 따른 방식을 Ducktyping이라 한다.\
Go와 같은 Statically Typed Language에서 Interface 등을 사용하여 기능을 구현하는 것을 Generics라고 한다.

---

# Ajax의 장단점
장점
* 웹페이지 로드 속도 향상
* 서버의 처리가 완료될 때까지 기다리지 않고 처리 가능
* 서버에서 Data만 전송하면 되므로 전체적인 코딩 양 감소
* 기존 웹에서 불가능했던 반응성 구현 가능

단점
* 히스토리 관리 불가
* 서버의 부하 증가 가능
* XMLHttpRequest를 이용하여 사용자에게 요청 진행상황에 대한 정보가 주어지지 않음

---

# TDD
Test Driven Development(테스트 주도 개발)
1. 테스트 코드 작성
2. 테스트 실패
3. 성공을 위한 최소한의 코드 작성
4. 코드 리팩토링

모든 기능에 대해서 테스트를 한다면, 어떠한 Method, Class를 개발한 후, 이를 사용하는 Method, Class에서 동작하는지를 확인해야 하기 때문에 시간이 오래 걸린다. Unit Test\
전체 서비스가 동작한다면 각각의 기능에 문제가 없을 가능성이 높다. 하지만 가능성일 뿐이다. Integrated Test\
따라서 모듈별로 테스트를 하는 것을 추천한다. 모듈은 그 자체로서 마이크로 서비스이며, 데이터를 캡슐화하여 API로만 데이터를 제공한다.\
모듈에서 유닛테스트를 진행하고, 전체 서비스를 테스트할 때는 코어 로직을 테스트한다. 코어 로직이 아니라면 유저에게도 큰 의미가 없기 때문에\
또한 모듈을 테스트할 때는 모듈의 정의, Dependency를 최소한으로 한다.\
데이터베이스를 사용한다면 인메모리의 데이터 스트럭쳐(해쉬맵) 등을 사용해서 데이터베이스의 기능을 흉내내거나, 다른 모듈의 API를 콜한다면 이를 위한 가짜 함수를 만드는 식으로 해당 모듈 밖의 관여를 최소화한다.\
이 테스트가 완료된 후에 필요한 라이브러리, 기타 모듈을 실제 로직에 대입한다.\
중요한 것은 테스트를 하는 중에도 데이터를 캡슐화하여 API를 통해서만 모듈을 테스트하는 것이다.\
테스트 코드를 작성할 때, 중요한 것은 다른 개발자들에게도 '읽히기 쉽도록' 정보를 최소한으로 제공하는 것이다.\
실제 데이터를 매번 construct하는 것보다, 저장된 데이터 중 'NEW'인 것과 같이 최소한의 정보만 제공하는 것이 유지 보수에 좋다.\
테스트에 다른 URL이나 다른 모듈의 API를 제공해야 할 경우를 대비해서, 테스트에 간단한 Endpoint API를 만들어 놓는 것이 좋다.

---

# OOP
OOP 원칙
* SRP(Single Responsibility Principle) : 단일 책임 원칙, 한 클래스는 하나의 로직에 대한 것이어야한다.
* OCP(Open Clos Princile) : 개방 폐쇄의 원칙, 클래스는 확장에는 열려있고, 변경에는 닫혀 있어야 한다는 원칙
* LSP(Liskov Substitution Principle) : 리스코프 치환의 원칙, 서브 타입은 언제나 기반 타입으로 교체할 수 있어야 한다라는 원칙. 쉽게 설명하면 부모가 동작하는 기능은 자식도 동일하게 동작해야 함
* ISP(Interface Segregation Principle) : 인터페이스 분리의 원칙, 자신이 사용하지 않는 인터페이스는 구현하지 말아야 한다는 원칙. 바꿔 말하면, 하나의 큰 인터페이스보다는 여러개의 작은 인터페이스를 구현하는 것이 낫다
* DIP(Dependency Inversion Principle) : 의존 관계 역전의 원칙. 구조적 디자인에서 발생하던 하위 레벨 모듈의 변경이 상위 레벨 모듈의 변경을 요구하는 위계관계를 끊는 의미의 역전. 쉽게 말하면 코드에서는 인터페이스에서 구현하는 클래스로 그 의존 관계가 흐르지만 실행시에는 역전된다.


---

# Stream
스트림은 추상화된 장치이다. 여러가지 주변 장치(모니터, 키보드 등)을 추상화 시켜서 사용자가 마치 동일한 장치에 접근하는 것처럼 사용할 수 있게 만들기 때문.

---

# TDD Pros and Cons
장점
1. 코드의 품질 향상 - 지속적으로 테스트를 하면서 QA를 거치지 않고도 어느정도 테스트를 보장할 수 있음
2. 테스팅 코드를 작성하며 문서화 작성도 도움

단점
1. 높은 러닝 커브
2. 테스트 코드를 만드는 비용(시간) 소요

널리 사용되는 TDD Framework는 Junit(JAVA), DocTest(Python) 등이 있다.
C에서 사용하기 위해서는 직접 만들어서 사용할 수도 있다.

	#include <stdio.h>
	int tests_run = 0;
	
	#define FAIL() printf("\nfailure in %s() line %d\n", __func__, __LINE__)
	#define _assert(test) do {if (!(test)) { FAIL(); return 1; } } while(0)
	#define _verify(test) do {int r=test(); tests_run++; if(r) return r; } while(0)
	
	int square(int x);
	
	int square_01() {
		int x = 5;
		_assert(square(x) == 25);
		return 0;
	}
	
	int square_02() {
		int x = 3;
		_assert(square(x) == 33);
		return 0;
	}
	
	
	int all_tests() {
		_verify(square_01);
		_verify(square_02);
		return 0;
	}
	
	int main(int argc, char **argv) {
		int result = all_tests();
		if (result == 0)
			printf("PASSED\n");
		printf("Tests run: %d\n", tests_run);
	
		return result != 0;
	}
	
	int square(int x) {
		return x*x;
	}

---

# IoC & DI
Inversion of Control은 사용자가 생성하는 애플리케이션이 프레임워크의 메소드를 Call하지 않고, 오히려 프레임워크가 애플리케이션이 제공하는 로직을 사용하는 것이다.

	# Python Example
	Class SomeClass:
		def __init__(self):
			self.some_obj = SomeObject()
		...

	# 위의 예에서 SomeClass 객체는 SomeObject 객체를 만들게 된다.
	# IoC를 적용한 코드는 아래와 같다.
	Class SomeClass:
		def __init__(self, some_obj):
			self.some_obj = some_obj

이름처럼 flow control의 주체를 역전할 수 있다.\
첫번째 예시는 SomeObject와 SomeClass 사이에 의존성을 만듦으로써 기존에 존재하는 코드에 필요한 Logic을 주입하는 것을 어렵게 만든다.\
대부분의 Framework는 두번째 예시와 같은 방식으로 어떠한 객체를 생성하고 이를 Flow를 제어하는 객체에 넘겨주는 형태를 가지고 있다.

Dependency Injection은 IoC의 한 형태이다.\
위의 예시와 같이 constructor/setter를 통해서 로직을 제공하는 것을 뜻한다.\
DI가 아닌 IoC의 예는 XML 등의 파일을 사용하여 프레임워크에 로직을 제공하거나(NginX), Child Class를 생성함으로써 프레임워크에 로직을 제공하는 행위(Web Frameworks like Flask, etc) 등이 있다.

---

# Multiprocessing Pros and Cons
장점
* 동시성을 구현해서 리소스를 더 효과적으로 사용할 수 있다.

단점
* 멀티프로세싱의 경우 메모리의 주소가 같게 나오더라도 사실 다른 주소에 밸류가 저장되어 있다. 메모리를 배로 사용하며, 접근하기 힘들다. 이를 막기위해서는 Multiprocessing을 위한 메모리를 따로 구성하고 이를 통해서 멀티프로세싱을 해야한다.
* 효과적인 멀티프로세싱을 구현하는 것은 악명이 있을만큼 어렵다.

아래는 Python 멀티프로세싱 예시

	import os
	import time
	glob = 0
	
	def main():
		global glob
		target = 0
		print('It should be only printed once')
		pid = os.fork()
		if pid == 0:
			for _ in range(100000):
				target += 1
				glob += 1
			print('PID:0 Address of Target: {}'.format(hex(id(target))))
		else:
			for _ in range(100000):
				target -= 1
				glob -= 1
			print('PID:{} Address of Target: {}'.format(pid, hex(id(target))))
		print('Address of Target: {} Target Status: {}'.format(hex(id(target)), target))
	
	if __name__ == '__main__':
		main()
		print('Global Value: {}'.format(glob))

위의 예시에 대한 출력값은 항상 같게 나타난다.

	It should be only printed once
	PID:13251 Address of Target: 0x7f4b70715d10
	Address of Target: 0x7f4b70715d10 Target Status: -100000
	Global Value: -100000
	PID:0 Address of Target: 0x7f4b70715c30
	Address of Target: 0x7f4b70715c30 Target Status: 100000
	Global Value: 100000

반면 스레드는 공유 메모리와 개인 메모리가 있다. 스레드는 지역변수가 존재하는 Stack을 제외한 모든 부분을 공유한다.

	from threading import Thread
	target = 0
	
	def plus_one():
		global target
		for _ in range(100000):
			target += 1
	
	def minus_one():
		global target
		for _ in range(100000):
			target -= 1
	
	def main():
		threads = []
		threads.append(Thread(target=plus_one))
		threads.append(Thread(target=minus_one))
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		print(target)
	
	if __name__ == '__main__':
		main() 

위 코드의 출력값은 0이 나올 수도 있지만 일반적으로 계속해서 다른 값이 나오게 된다.\
이를 막기위해서 Mutex, Semaphore 등의 Lock을 사용한다.

---

# Traffic Overflow
예를 들어 서버가 초당 10만건의 요청을 수행할 수 있는데, 현재 서비스의 피크 타임에는 초당 100만건의 요청이 들어온다. 어떻게 처리할 것인가?\
*가장 쉬운 방법은 인프라 레벨에서 처리하는 것일 것 같음*
* 서버의 스냅샷을 만들어서 오토스케일링한다. 서버의 앞단에는 로드밸런서를 두어서 트래픽을 각 서버에 분산할 수 있도록 설정한다.
* BE를 컨테이너로 만들어서 K8S 클러스터를 설정하고 그 안에 띄운다. 쿠버네티스는 서비스의 이름으로 (기본적으로 Round Robin 방식) 로드밸런싱이 되며, 서비스의 갯수를 자동으로 오토스케일 할 수 있으므로 위의 사항을 모두 만족할 수 있다.
*리소스에 제한이 있다면 소프트웨어적으로 처리한다*
* 반드시 실시간(0~1초 응답)이 아니라면 Rabbit MQ, Redis를 사용하거나 AWS SQS와 같은 서비스를 이용하여  큐를 만들어서 서버가 순차적으로 요청을 처리할 수 있도록 한다.
* 코드의 로직을 Async로 바꾸면 요청의 블로킹 부분에서 의미없이 낭비되는 시간을 줄여서 더 많은 Request를 처리할 수 있다.
* HTTP/2는 Stream Priority를 다룰 수 있다. 더 중요한 요청을 처리하는 Stream을 따로 관리한다.

---

# Stack Overflow
메모리의 스택 영역에 참조된 주소값이 주어진 영역 밖으로 나갈 때 발생하는 에러 (Stack Overflow는 해당 스코프의 지역 변수를 관리한다.)
* 재귀 함수의 End Condition을 잘못 설정해서 무한대로 재귀를 하게 되면 Stack Overflow 발생
* double test[10000000000]; (size = 8bytes\*10000000000 = 80Gb)와 같이 메모리를 너무 많이 사용하게 될 때도 Stack Overflow 발생

---

# POSIX
Unix 기반의 운영체제에서 지원하는 프로그래밍 인터페이스 기준

---

# UTF8
ASCII는 0~255에 각 알파벳 문자를 매칭하여 영어가 아닌 다른 문자를 사용하는 나라에서는 각자의 인코딩을 개발했다.(~196?)\
하지만 Web이 탄생하면서 세계적으로 데이터 통신을 하는 경우가 많아졌고, 이를 위해서 UNICODE가 탄생한다. UNICODE는 모든 문자열을 숫자로 치환하면서 한 문자열을 최대 21개의 비트로 나타낸것이다. 하지만 문제점이 있다.
1. 문자열을 나타내는데 필요없는 비트가 너무 많다.
2. 한 바이트에서 모든 비트가 0인 경우 EOF, NULL이라고 취급하는 컴퓨터와 Backward-Compatibility가 안된다.
따라서 UTF-8 인코딩이 Norm이 되었다.

	110xxxxx 10xxxxxx 과 같이 가장 먼저 오는 바이트가 앞으로 몇 바이트 동안 한 문자열을 나타낼 것인지 정한다.\
	1110xxxx 10xxxxxx 10xxxxxx 와 같이 최대 1 + 6\*6 비트를 나타낼 수 있으며, 각 문자열은 낭비되는 양을 최소화하므로 효과적이다.

---

# 서버의 LifeCycle
1. Socket 생성 - 소프트웨어의 데이터 송수신을 책임지는 OS의 단위. LINUX에서 모든 것은 파일이다.
2. Bind - 서버의 IP주소와 포트를 소켓에 할당한다.
3. Listen - 특정 주소에 Bind된 소켓을 Request에 응답 가능한 대기 상태로 만들기
4. Accept - 클라이언트로부터 해당 소켓에 Request가 도착했을때, 수락
5. Read/Write - 일반적인 File IO와 같이 필요한 데이터를 해당 소켓(파일)에 읽고 쓰기
6. Close - 연결 종료

---

# POSIX Poll vs Select
select와 poll 모두 fd의 묶음을 모니터하지만, select의 fd set은 bit mask 형식을 띄기 때문에 따로 설정하지 않을 경우, 1024개의 고정된 크기를 가진다.\
poll은 pollfd라는 구조체를 통해서 모니터하며, poll 함수 자체에 length를 인자로 넣기 때문에 크기에 한계가 없다.\
근래에는 poll이 select의 기능을 모두 대체하므로 select는 deprecate 되야 한다는 의견이 있다.\
epoll을 사용하여 waiting 중에도 fd를 추가하거나 제거할 수 있다.\
또한 epoll은 O(1)로 접근가능하지만, Linux에서만 epoll API를 제공한다.

---

# Use of sockaddr\_in.sin\_zero
짧게 말해서 struct sockaddr과 같은 사이즈를 유지하기 위해서 zero padding이 필요하다.\
대부분의 네트워크에 사용되는 코드는 sockaddr\_in이 아닌 sockaddr 구조체를 사용한다.\
POSIX의 sendto 같은 function을 사용할 때도 sockaddr로 타입캐스트 후 sockaddr\_in을 사용한다.\
앞의 이유로 sin\_zero가 필요하다. 크기를 맞춰야 형 변환을 했을 때 이상한 값이 들어가지 않을테니까.\
어떤 시스템에서는 zero padding을 하지 않아도 문제가 없지만, 어떤 시스템에서는 문제를 일으킬 수 있으므로 반드시 필요하다.\
sockaddr은 unsigned short sa\_family와 char sa\_data[14]를 가지므로 16바이트를 맞추기 위해서 char sin\_zero[8]이 필요한 것이다.

---

# TDD Tool의 중요성
UNIX socket programming을 연습하려고 로드밸런서 예제를 만드는데, TDD를 위해서 테스트 코드를 만들다보니 C에서 테스트코드를 직접 다루기가 상당히 불편하다는 사실을 배웠다.\
이미 만들어진 소켓 서버에 소켓 클라이언트를 연결하고 제대로 동작하는지 보려는 Module 단위?의 테스트인데, C안에서 구현하려다 보니 테스트코드가  실제 코드만큼 길어지는 걸 보고 중지했다. 퍼포먼스의 문제는 있겠지만 테스트는 Doctest(Python) 같이 외부의 프레임워크를 사용하는게 편의성 면에서 더 나을 것이라고 생각한다.\
지금까지는 테스트코드를 직접 만들어서 사용하고, TDD Tool을 잘 사용하지 않았는데 코드의 크기가 클수록 tool을 사용하는게 나을 것 같다.

---

# epoll
* Level-triggered는 watched file descriptor가 ready state가 아니게 될 때까지 계속해서 이벤트를 받는다. (default)
* Edge-triggered는 watched file descriptor의 state가 변했을 때만 이벤트를 받는다.

기본 흐름\
epoll instance는 file descriptor이다.\
해당 epoll instance에 epoll\_ctl call을 통해서 어떤 fd의 어떤 이벤트를 어떻게 할 것인지를 설정한다.\
이후 epoll\_wait call을 통해서 epoll instance에서 한 번에 최대 몇 개의 이벤트를 받고 얼마의 Timeout을 줄 것인지 설정한다.\

*epoll을 통해서 서버를 구성한다면, 무슨 장점이 있을까? Socket 역시 fd이므로 listen을 하는 서버는 한 번에 한 event만 다루는게 아닌가? 하지만 예시를 보면 한 서버의 socket에 대해 epoll_wait을 할 때도 많은 event를 받는 것으로 나와있다. socket fd에 오는 모든 event를 epoll instance가 "다" 기억하는 것으로 예상된다. 그렇다면 epoll을 쓰는 데 확실히 장점이 있다. epoll을 쓰지않은 서버는 동시에 다수의 연결이 동시에 구성되고 쓰레드를 만들어서 연결을 전해주고 다시 accept하기 전에 모든 요청이 왔다 갔다면 그 중 한 개만 수행될테니까. 반면 epoll을 사용한다면 현재 랩톱에서도 (file-max에 따르면, 리소스가 충분하다면) 수천조 이상의 fd를 관리할 수 있을 것이다.*

*epoll은 커널에서 이벤트 데이터를 보관한다. 만약 MAX_FD를 실제 이벤트보다 낮게 설정했더라도 이벤트는 Queue에 남아 다음 번 wait에서 불러오게된다. 또한 다른 스레드가 epoll_wait을 하고 있더라도 epoll_ctl을 통해서 수정이 가능하다.*

---

# File Descriptor
FD는 UNIX 계열 OS의 열린 파일을 identify하는 unique한 숫자로, 데이터 소스와 액세스 방식에 대한 데이터를 포함한다.\
어떠한 프로그램이 데이터 소스를 열거나, 네트워크 소켓을 생성하면 커널은 아래와 같은 순서로 작업을 수행한다.

1. Access를 승인한다.
2. Global File Table에 entry를 생성한다.
3. 프로그램에 entry의 주소를 제공한다.

FD는 음수가 아닌 unique한 정수의 형태를 띄며, 시스템 상의 모든 열린 파일에 대해 최소 한 개 이상의 FD가 존재한다.\
Global File Table의 Entry는 inode(Index Node, 파일에 대한 정보를 포함), byte offset(바이트의 사이즈), access restriction(read-only, write-only, etc) 정보를 제공한다.\
기본적으로 0(stdin), 1(stdout), 2(stderr)은 할당되어 있다.

---

# Maximum Number of Connections in TCP
Whatsapp의 경우 한 서버에서 삼백만 Connection을 다룸.\
클라이언트는 약 2^16개의 Connection이라는 한게가 있지만, 서버의 경우 리소스만 충분하다면 제한된 Connection의 수는 없다.\
Proxy/Reverse Proxy를 사용하는 경우, 기술적으로 Proxy/Reverse Proxy가 클라이언트의 역할을 하기 때문에, 문제가 생길 수 밖에 없음(소켓을 사용한 Layer4 Proxy의 경우)\
해결책으로 Proxy/Reverse Proxy가 HTTP2를 사용하게 한다.(Eg. Envoy Proxy) Connection 안에서 많은 Stream을 생성하여 백과 통신하게 한다.\

---

# Signal
프로세스에게 어떤 조건/이벤트의 발생을 알리는데 사용되는 테크닉\
예를 들어 프로세스가 division by 0를 실행하면 SIGFPE signal이 해당 프로세스에 전달된다.\
시그널을 전달받은 프로세스는 아래 세 가지 방식으로 시그널에 대처한다.

1. 시그널을 무시한다.
2. Default 행동을 실행한다. 예를 들어 division by 0의 default action은 프로세스를 죽이는 것이다.
3. 시그널을 catch할 함수를 제공한다.

일반적으로 kill 명령어를 사용하여 프로세스에 시그널을 전달할 수 있으며, Ctrl\+C 같은 interrupt key 역시 시그널이다.

---

# System Call VS Kernel
모든 운영체제는 프로그램이 Kernel에 명령을 전달하도록 서비스 포인트를 제공한다.\
유닉스 기반의 운영체제에서 이러한 서비스 포인트를 System Call이라고 부르며 C로 커널 명령어 - C 함수가 1대 1로 매칭되도록 짜여져 있다.\
일반적인 라이브러리 함수와 시스템 콜의 차이는 라이브러리는 대체할 수 있는 반면, 시스템 콜은 (일반적으로) 대체할 수 없다는 점이다.\
예를 들어 메모리 할당을 위한 malloc은 다른 방법으로 대체될 수 있지만, UNIX System Call인 sbrk(2)는 대체할 수 없다.

---

# Simple Rules of Cleaner Code
* Variable의 이름을 명확하게 짓는다.

	int e; // elapsed time in days
	int elapsed_time_in_days; // 명확한 변수의 이름

* Comment에 의지하는 것보다 코드를 한 눈에 알아볼 수 있도록 짜는 게 중요하다.

* Boyscout Rule, Code를 처음 접했을 때 보다 더 clean하게 만들어야한다.

* Single Responsibility, it does one thing well, and it only does that thing.

* Write Tests, TDD에 따른 코딩이 더 나은 코드를 만든다.

---

# Nonblocking I/O
프로세스는 File Descriptor를 통해서 Pipe, File, Event Queue 등의 I/O를 참조한다. 데이터의 전달은 모두 Descriptor의 read/write를 통해 이뤄지기 때문에 이에 대한 이해가 중요하다.\
이러한 Descriptor는 부모 프로세스로부터 상속받거나 open, pipe, socket과 같은 system call을 통해서 생성한다.\
생성된 Descriptor는 아래와 같은 상황에서 release된다.
1. 프로세스 exit
2. close system call 호출
3. descriptor가 close on exec로 설정되었을 경우 exec system call 후 implicitly

프로세스가 fork를 하면 모든 descriptor는 복사되어 child에게 전달된다.\
만약 어떠한 descriptor가 close-on-exec으로 설정되었다면 부모가 fork를 호출하고, 자식이 exec되기 전에 자식에게 전달된 descriptor는 close되고, 따라서 자식은 해당 descriptor를 사용할 수 없게 된다.\
Descriptor는 File Entry라는 데이터구조를 가르키며, open system call이 새로운 file entry를 생성한다.\
Fork system call을 사용할 경우 부모와 자식 프로세스는 descriptor를 share by reference 형태로 공유한다.\
이렇듯 여러 file descriptor가 한 file entry를 공유할 수 있으므로, file entry는 각각의 file descriptor를 위한 file offset(cursor의 위치)를 기억해야 한다.

File Entry는 아래와 같은 데이터를 포함한다.
* 타입
* 함수 포인터들의 배열 (fd에 대한 ops를 file-specific으로 전환한다.)

기본적으로 어떠한 descriptor에 read, write, send를 할 경우 데이터가 없다면 block이 된다. disk files를 제외한 fd에 대한 대부분의 ops는 block된다. (disk files의 경우 kernel buffer cache를 통해서 이루어지기 때문에 block되지 않는다.)\
disk write이 sync하게 작동할 때는 disk file을 open시 O\_SYNC flag가 주어졌을 때이다.\
Pipe, FIFO, socket을 포함한 모든 descriptor는 nonblocking mode로 사용될 수 있다.\
Descriptor가 non-blocking 모드일 때, 해당 descriptor에 대한 IO system call은 즉시 완수할 수 없더라도 바로 return된다.\
이 때 반환되는 값은 아래 중 하나이다.
* error: ops가 전혀 수행될 수 없을 때
* partial count: ops가 일부분 수행될 수 있을 때
* entire result: IO 전체가 완전히 수행될 수 있을 때

descriptor는O\_NONBLOCK flag를 설정함으로써 non-blocking 모드로 열린다.\
descriptor는 IO operation을 블록없이 수행할 수 있을 때, ready 상태로 여겨진다.

---

# Edge Trigger VS Level Trigger (Simple)
* Level Trigger: 언제든 fd가 read-available하다면 이벤트를 받는다.
* Edge Trigger: fd가 read-available하게 된 순간 이벤트를 받는다.
ET-System에서는 fd가 available하지 않다가 available하게 된 순간 이벤트를 받는다. 제공받은 이벤트에서 일부분을 읽었다면, (아직 읽지 않은 부분이 있어도) 이벤트를 다시 전달받지 않는다. 모든 데이터를 읽고 다른 데이터가 fd에 전송되었다면 그 때 다시 이벤트를 전달받는다.\
반면 LT에서는 데이터가 available 할 때는 언제나 이벤트를 전달받는다.

---

# FILE I/O in UNIX
UNIX 시스템에서 대부분의 file io는 open, read, write, lseek, close 5개의 함수로 수행할 수 있다.\
프로세스는 process table entry에 fd와 file pointer를 저장하고, file pointer는 다시 file table entry에 있는 file status flags, current file offset, v-node pointer를 가리킨다. 여기서 v-node는 i-node를 i-node는 v-node를 가리킨다.\
만약 서로 다른 두 프로세스가 한 파일을 open한다면, 서로 다른 file table entry가 같은 v-node table entry를 가리키는 방식으로 실행된다.\
dup, dup2 함수를 통해서 기존의 fd를 복사할 수 있다. 이렇게 복사된 fd는 같은 프로세스에서 하나의 file table entry를 공유한다. 이것은 fcntl을 F\_DUPFD를 사용하여 같은 결과를 낼 수 있다.\
*fcntl은 두 번의 함수 호출이 필요하지만, dup은 atomic하다. 따라서 컨텍스트 스위치 등으로부터 안전하게 프로세스가 진행된다.*

---

# I-NODE VS V-NODE
V-node는 모든 파일 시스템에 대해서 추상화를 제공하여 커널이 모든 파일시스템을 지원하지 않아도 OS가 해당 파일시스템과 상호작용 할 수 있도록 돕기위해 만들어졌으며 In-memory에 저장된다. 또한 V-node에 저장되는 정보는 파일에 대한 정보를 저장하지만, 파일의 lifespan에 변경되지 않는 데이터만 저장한다.(inode에 대한 정보 등)\
반면 I-node는 on-disk에 저장되며, 사용되는 파일 시스템에 종속된다. Inode는 파일 사이즈, 소유자, 파일의 물리적  주소(포인터) 등 파일에 대한 메타데이터를 포함한다.

---

# Hard Link VS Symbolic Link
파일 시스템의 파일은 기본적으로 inode를 가리키는 링크이다.\
하드링크는 original 파일이 가리키는 inode를 가리키는 새로운 파일이다. 같은 file system 안에서만 유효하다.\
따라서 하드링크는 original의 데이터가 바뀌어도, 위치가 바뀌어도, 심지어 original이 삭제되어도 원래 inode가 가리키는 데이터를 보존한다.(original을 수정하면 hard 역시 수정된다. 모든 링크가 삭제되기 전에는 inode는 삭제되지 않는다.)\
반면 심볼릭 링크는 파일시스템의 다른 파일 이름에 대한 링크이다.\
따라서 original의 이름이 바뀌면 심볼릭 링크는 더 이상 해당 파일을 가리키지 못한다. inode가 아닌 다른 파일의 이름을 가리키므로, 다른 file system 안에서도 동작한다.

---

# Files and Directory in UNIX
* Regular File: 가장 일반적인 파일 타입. 데이터의 형태가 텍스트/바이너리인지에 대한 구분이 없다. 데이터에 처리는 Application에 따라 다르다. Binary Executable인 경우에는 커널이 인식할 수 있는 format을 따른다.
* Directory File: 다른 파일들의 이름과 정보에 대한 포인터를 포함한 **파일**
* Block Special File: 디스크 드라이브 등의 device에게 buffered I/O를 제공하는 파일 형식
* Character Special File: device에게 unbuffered I/O를 제공하는 파일 형식. 모든 device는 block special 혹은 character special file 중 하나이다.
* FIFO: 프로세스간의 communocation에 사용되는 파일의 타입. Pipe라고 불리기도 한다.
* Socket: 프로세스 사이의 네트워크 통신에 사용되는 파일 타입.
* Symbolic Link: 다른 파일을 가리키는 파일 타입.
POSIX는 message queue, semaphore, shared memory object 같은 IPC\(interprocess communication\) 객체도 파일 타입으로 명시해두었지만, UNIX System implementation에 따라 IPC 객체를 실제로 file로 나타내는지는 다르다.

어떠한 파일을 파일 이름을 통해서 열 때, 항상 이름에 포함되어 있는 모든 dir에 execute 권한을 가지고 있어야된다.\
하지만 디렉토리에서 read와 execute 권한은 서로 다르다.\
read 권한은 directory를 읽고 dir내의 모든 파일이름을 읽는데 사용되며, execute 권한은 directory 내에서 활동을 가능하게 한다.(rw-인 경우에는 ls 허용, cd dir 불가/ -wx인 경우에는 cd dir 허용, ls 불가/ write를 위해서는 w와 x 모두 필요)\
sticky bit을 설정하면 첫 실행 후 파일을 swap area에 복사하여 보관한다. 일반적인 UNIX file system의 랜덤한 데이터 블록에 저장되는 성질과는 반대로 swap area의 파일들은 연속적인 파일로 인식되므로 더 빠르게 실행할 수 있다. sticky bit은 유닉스 시스템의 버젼이 높아지면서 saved-text bit(svtx)로 이름이 바뀌게 되었으며, virtual memory system과 효율적인 file system 덕분에 saved-text bit은 자주 사용되지 않게 되었다.\
최근에는 sticky bit을 dir에 설정하게 되면 dir내의 파일은 사용자가 dir에 대해 쓰기 권한을 가지고 있으며, 파일의 owner이거나, dir의 owner이거나, root 일때만 지우거나 rename 할 수 있는 설정이  추가되었다.

---

# Standard I/O
Buffering은 세가지로 분류할 수 있다.
* Fully Buffered: Disk의 파일들은 일반적으로 Standard IO Lib에 의해 fully buffered 된다. Buffer는 Standard IO function인 malloc을 통해서 설정된다. Buffer의 write는 flush에 의해서 결정된다. Standard IO Lib에서 flush는 buffer의 내용을 write하는 것이지만, terminal driver에서는 buffer의 내용을 버린다.
* Line Buffered: Input 혹은 Output에서 \\n(newline char)이 발생하면 IO를 수행한다. Line Buffer는 주로 터미널과 연결되었을 때, stdin, stdout, stderr 등에 사용된다. 하지만 Line Buffer의 크기가 fixed 되어있으므로 \\n를 만나기 전에 IO가 실행될 수도 있다.
* Unbuffered: Standard IO Lib이 buffer를 수행하지 않는다. fputs에 string을 입력하면, buffer없이 write function을 통해서 바로 데이터가 출력된다.

*terminal devices = line buffered, unbuffered = stderr*

---

# ABC(Abstract Class) in Python
상속받는 다른 class를 위한 blueprint.\
동일한 API를 여러 interface에 적용하기위해서 사용된다.

	import abc
	class Thing(metaclass=abc.ABCMeta):
		@abc.abstractmethod
		def test(self):
			pass
	
	>>> a = Thing()
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	TypeError: Can't instantiate abstract class Thing with abstract methods test

위에서는 test 메소드를 implement하지 않은 abstract class인 Thing을 직접 사용하려했으므로 런타임 에러가 발생한다.

---

# Python Super and List Comprehension Imcompatibility

	class Base:
		def __init__(self):
			# do something
	
	class Child(Base):
		def __init__(self):
			super().__init__()
			# do something

위의 코드에서 Child는 super()를 통해서 Base를 상속받는다. 이때 super는 아무런 parameter가 필요하지 않다. 왜냐하면 인터프리터는 super가 있는 위치가 Child 클래스의 __init__ 메소드의 스코프인 것을 알고 자동으로 입력해주기 때문이다.\

	class Base:
		def __init__(self):
			# do something
	
	class Child(Base):
		def __init__(self):
			tmp = [super().__init__() for _ in range(5)]
			# do something
	
	>> super(type, obj): obj must be an instance or subtype of type

하지만 위와 같이, list comprehension과 같은 자신의 스코프를 가지는 블록 안에 super를 호출하면 인터프리터가 어떤 값을 넣어야되는지 몰라서 에러가 발생하게 된다.

---

# Go Mod

	$ go mod init [module name] // init go module in the current dir, making go.mod file
	$ go get [package] // get pkg and add it to go.mod, which tracks pkgs, and go.sum will be created, which tracks pkgs' dependencies
	$ go mode tidy // remove un-used pkgs, add missing pkgs

go module은 v0(unstable)과 v1(stable)만 기본적으로 지원한다. 따라서 Major Version은 아래와 같은 사용법을 가진다.

	$ go get rsc.io/quote@v1.3.0 // correct
	$ go get rsc.io/quote@v3.0.0 // incorrect
	$ go get rsc.io/quote/v3 //correct

---

# Go Vendor
vendor dir은 $GOPATH/src와 같은 structure를 가진다.\
vendor dir내에 src에서 사용하는 pkg가 있을 경우, $GOPATH보다 vendor의 pkg를 먼저 사용한다.\
만약 vendor가 recursive하게 구성되어 있다면, 가장 안에 있는 vendor dir의 pkg를 사용하게된다. 하지만 nested vendor dir은 권장하지 않으므로, 되도록 사용하지 않는다.

go get은 vendor를 update하지 않는다. 따라서 3rd party app을 사용하여 vendor dir을 관리한다.

---

# Drawback of Client Side Rendering
일반적으로 서버의 overhead를 줄이기 위해서 client side rendering을 사용한다.\
현재는 client side rendering이 norm이 되어서 실제 html에는 사용할 script, img 등이 들어있을뿐, 데이터는 없는 경우가 많다.\
하지만 robot이 crawling을 하거나, 링크의 preview가 생성될 때를 생각해보면 empty html을 사용할 수 없다.\
이를 막기위해서는 html 자체에 meta data를 hardcode하거나, server side rendering을 할 수 밖에 없다.

	user -> front(web) -> back(was) // 방법 1: front가 back의 데이터로 html을 생성해서 user에게 돌려준다. 어떻게 보면 렌더링 기능이 추가된 reverse proxy같이 작동한다.
	// 방법 2: front의 nginx의 proxy_pass 등을 통해서 back에서 html을 렌더링하여 반환하도록 한다.
	// 방법 3: front에 react-snap 등을 사용하여, page의 snapshot을 생성하고 이를 반환하게 한다.
	// 방법 4: request의 user-agent를 읽어서 user의 접근일 경우, client side rendering, bot의 접근일 경우, hard-coded data제공
	
application의 필요에 맞춰 server side rendering / client side rendering을 선택해야한다.

---

# OAuth
A Site의 User에게 B Site의 Auth 권한을 제공하는 Framework\
OAuth 순서는 아래와 같다. 

1. Authorisation Request (to Resource Owner)
2. Authorisation Grant (from Resource Owner)
3. Authorisation Grant (to Authorisation Server)
4. Access Token (from Authorisation Server)
5. Access Token (to Resource Server)
6. Protected Resource (from Resource Server)

	// Example
	//1
	//Resource Owner, Auth Service를 제공하는 대상, 즉 User에게 auth 수단을 요구한다. (id 등)
	return res.redirect(AUTH\_URI + '?client\_id=' + CLIENT\_ID + '&redirect\_uri=' + CALLBACK\_URI + '&response\_type=code' + '&scope=' + RESOURCE\_TO\_GET);
	
	//2
	//Resource Owner는 Auth 수단을 Application(Client)에 제공한다.
	
	//3
	//2에서 전달받은 Auth Grant(수단)를 Authorisation Server에 전달한다.
	let auth = await request
		({
			method: 'post',
			url: Authorisation Server URI,
			headers: {
				...
			},
			form: {
				code,
				client_id: CLIENT_ID,
				client_secret: CLIENT_SECRET,
				...
			},
			...
		});
	...
	
	//4
	//3을 통해서 Application(Client)는 Authorisation Server로부터 Access Token을 제공받는다.
	
	//5
	//4에서 받은 Access Token을 포함하여 Resource Server에 요청을 보낸다.
	
	//6
	//Resource Server는 Token이 일치하는지 확인 후 Resource를 제공한다.

OAuth를 사용하기 위해서는 Auth를 제공하는 Service에 application을 등록해야 한다.\
이를 통해서 제 3자가 Malicious Link를 통해서 User의 Token을 빼내려 하더라도 Service 측에서 공격을 방지한다.\
위의 Client ID와 Client Secret은 Service에 Application(Client)를 등록하면 Service가 제공한다.\
OAuth 프레임워크가 많이 있지만, 스스로 Implement해도 수십 Line의 코드일 뿐이므로 스스로 적용하는 것도 좋다.\
대부분의 Oauth Service Provider는 OAuth Guide를 제공하므로 참조하여 사용한다.

---

# How to Store JWT

	Client -> Login -> Server
	Client <- accessToken, refreshToken <- Server
	
	// accessToken은 Memory에, refreshToken은 cookie에 저장한다.
	// Server에 Request를 보낼 때, accessToken은 authentication header에, refreshToken은 body에 넣어서 전달한다.
	// Server는 accessToken이 valid하면 response를 전달한다.
	// 하지만 accessToken이 만료되거나, User가 Refresh 했을 경우에는 accessToken이 유효하지 않다.
	// requestToken은 Refresh Request를 보낼 때에만 accessToken을 반환하므로 공격을 무력화한다.
	
	// Client가 refresh 후 Server에 접근하면 (refresh request), Server는 valid accessToken을 발행한다.
	// accessToken이 expired 되었을 경우 invalid request / expire header를 보고 Refresh Request를 보내게 된다.

---

# Golang SQL package
다른 언어, Lib과의 차이점은 일단 Single Query의 경우 commit을 자동으로 수행하며, 여러 Query가 합쳐진 Transaction은 Transaction을 선언한 후 Exec, Commit, Rollback 과정을 거친다는 점.\
또한 다수의 Entry가 반환되는 Query의 경우, Rows라는 Interface를 반환한다. Rows는 Next() Method를 통해서 다음 Rows에 대한 정보를 Lazy Evaluation하는데, 특이하게도 아래와 같은 Syntax를 취한다.

	for rows.Next() {
	    val (
	        n string,
	        m int
	    )
	
	    rows.Scan(&n, &m)
	    u := model.User{Name: n, Age: m}
	    models = append(models, u)
	}

위와 같이 rows.Next()를 실행한 상태로 그 안의 scope에서 해당 row를 처리하는 것을 best practice(이자 golang의 일반적인 package가 그렇듯 유일한) 처리 방법으로 두고 있다.\
아직 SQL pkg의 소스 코드를 까보지는 않았는데, Next()는 -1 idx에서 시작해서 늘어가는 거겠지

또 MySQL의 timestamp는 time pkg의 time.Format(time.RFC3339)와 compatible하다. time.Time type이기 때문에 JSON Marshal에도 문제가 없다! 땡큐!

---

# Go\'s String & Byte & Rune
Go의 source code는 utf-8을 사용한다.\
따라서 string literal은 utf-8 인코딩된 문자열을 나타내게 된다.\
하지만 string은 arbitrary byte의 array이므로 모든 string이 utf-8 value만 가지는 것은 아니다.

예를 들어 ⌘는 U+2318이며 \\xe2\\x8c\\x98로도 나타낼 수 있다.\
그렇기 때문에 string과 character에 대해서 나타낼때는 ambiguous 할 수 밖에 없다.

또한 à를 나타내기 위해서는 U+00e0을 사용할 수도 u+0300과 U+0061의 조합으로도 나타낼 수 있다.

이처럼 한 character를 나타내는 codepoint의 단위를 go에서는 rune이라 한다.

---

# Generics in Go
"Generic programming enables the representation of functions and data structures in a generic form, with types factored out..."\
아래 함수는 string 등 다른 []\<type\>에는 사용할 수 없다.

    func Reverse(s []int) {
        var (
            left = 0
            right = len(s) - 1
        )
        for left < right {
            s[left], s[right] = s[right], s[left]
            left++
            right--
        }
    }

아래와 같이 Interface를 통해서 generics를 흉내낼 수 있지만

    func Reverse(s []interface{}) {
        var (
            left = 0
            right = len(s) - 1
        )
        switch s[0].(type) {
            case int64:
                // do something
                ...

여전히 코드를 반복해야할 뿐아니라, Go의 Best Practice도 아니다.(Statically Typed Language의 강점이 사라진다.)\
Developer들의 요구로 Generics Implement를 고려하고 있지만, 우선순위가 아니며 Trade-off가 있기 때문에 확실하진 않다.

-> 위의 예시처럼 편리하긴 할테지만 Generics를 통한 overhead와 complexity가 golang에 적합한지는... 차라리 code generator를 사용하는게 나을 수도 있을 듯

---

# Streaming
얼마 전부터 궁금했던 streaming을 간단하게 구현하는 가이드를 따라서 구현을 해봤다.\
단순한 File Server를 제공하면 Protocol에 맞춰 video play framework가 HLS면 HLS, DASH면 Dash로 지원하는 형태였다.\
*HLS는 Apple이 개발한 format이라 그런건지 safari를 제외하면 접근성이 좋지 않은 것 같았다.*

	const songsDir = "song"
	const port = 9999

	http.Handle("/", addHeaders(http.FileServer(http.Dir(songsDir))))

Encoding, File Server(s3 Object Storage를 대부분 사용) 부분도 구현할 부분이 많이 있지만 내 생각에는 대용량 데이터인 비디오를 보관할 media server, edge-service provider 등 architecture를 제대로 구현하는게 속도와 안전성, scalability에 가장 포인트가 아닐까 생각한다.\
Front, 게다가 video framework를 사용해본적이 없어서 black box처럼 느껴지는 부분이 좀 있었고, web rtc가 이렇게 swiss army knife 같이 느껴질 줄은 몰랐다.\
단순히 File Server를 제공하는 게 아니라면 Logic은

    Client -> Streaming Server // 현재 status의 metadata request 후, 다음 status(vid) response
    // 여기서 중요한 점은 response가 highly available 해야한다는 점.
    // 또 Downtime도 없어야하지만, 다음 몇 프레임을 생략하더라도 그 다음 프레임을 볼 수 있는게 더 중요하지 않을까? (연속적인 비디오)
    // 이 기준이라면 UDP가 더 낫지만, HTTP3를 지원하는 프레임워크는 현재 한정적이므로, 아마도 UDP의 socket server를 직접 구현하는 것이 state-or-art가 아닐까 생각한다.

---

# All you need to know about wsgi
WSGI는 WebServer(NginX, Apache)와 Django, Flask 등의 Framework 사이에 존재한다.\
WSGI는 어떤 일을 하는가?

먼저 Classic한 웹 서버(CGI)는 아래의 flow를 따른다.\
WebServer는 Static Content를 반환하기만 하므로, Dynamic Content를 반환하기 위해서는 중간에 외부의 script를 동작시키고 이 결과값을 return 해줘야한다.\
이 과정에서 environment variable에 각종 param을 저장한 Webserver는 fork()하여 script를 동작시킨다.

WSGI는 CGI를 확장한 Gateway Interface이다.
어떠한 script라도 environment variable의 dict를 첫번째 argument로, 두번째 argument는 정해진 format에 따라서 함수 내에서 call하는 형식만 따른다면 webserver에 implement 될 수 있다.\
이것이 WSGI, webserver와 framework를 연결해주는 standard이다.

Apache의 경우 pre-forking을 통해서 최대한 fork()의 overhead를 줄인다.\
하지만 이러한 기능이 없는 NginX는 Gunicorn, uWSGI 등의 fork를 대신해주는 또 다른 웹서버에 forward해줌으로써 WSGI를 구현을 돕는다.

---

# Python High-order wrappers
* property decorator는 getter와 setter를 대신하는 역할을 한다.

	class Test():
	    def __init__(self, score = 0):
	        self.__score = score
	
	    @property # getter
	    def score(self):
            print('Getting score...')
	        return self.__score
	
	    @score.setter # setter
	    def score(self, value):
	        self.__score = value
    
    # >>> t = Test()
    # >>> print(t.score)
    # 0
    # >>> t.score = 42
    # >>> print(t.score)
    # 42

위와 같이 동작한다. property.deleter도 있다.

functools lib은 고계함수에 대한 지원을 하는 class, methods로 이루어져있다.\
* functools.cache는 function에 대한 cache를 구현한다.

    @cache
    def factorial(n):
        return n * factorial(n-1) if n else 1
    
    factorial(10) # 10까지 계산
    factorial(7)  # cache에서 retrieve

* functools.cached\_property는 method를 property로 만들고 그 값을 instance lifecycle 동안 cache한다.

    @cached_property
    def stdev(self):
        return statistics.stdev(self._data)
    
    # >>>print(something.stdev)
    # some data (cached)

* functools.lru\_cache는 functools.cache와 같지만 bound가 없이 무한히 커지는 cache와 다르게 maxsize(default 128)를 가진다. maxsize가 None으로 설정되면 cache와 동일하게 동작한다. typed flag가 true로 설정되면 type에 따라 다른 값으로 추정되어 cache에 저장된다.

* functools.partial은 partial object를 반환하며 partial object는 call 되었을 때 args와 kwargs가 설정된 함수처럼 동작한다.

    basetwo = partial(int, base=2)
    basetwo.__doc__ = 'Convert base 2 string to an int.'
    basetwo('10001')
    # 17

* functools.wraps는 wrapper function에 wrapped function의 메타데이터를 전달한다.

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper

    @decorator
    def example():
        """Docstring"""
        print('Called!')
    # >>> print(example.__name__)
    # 'example' # 사실 wrapper이지만 wraps를 통해서 변환
    # >>> print(example.__doc__)
    # 'Docstring' # 동일


---

# 7 Things to Remember When Use Concurrency in Go
1. 채널은 보내는 쪽에서 닫는다.
2. 보내는 쪽에서 반복문 등을 활용해서 보내다가 중간에 return을 할 수 있으므로 defer를 이용하는 편이 좋다.
3. 받는 쪽이 끝날 때까지 기다리는 것이 모든 자료의 처리가 끝나는 시점까지 기다리는 방법이므로 더 안정적이다. 생산자가 아닌 소비자가 끝내는 시점을 정하도록 한다. (생산자 생산 후 done, 소비자 소비 후 done, 모두 done)
4. 특별한 이유가 없다면 받는 쪽에서는 range를 사용하는 것이 좋다. 생산자가 채널을 닫으면 반복문을 빠져나오게 되므로 편리하다.
5. 루틴이 끝났음을 알리고 다른 쪽에서 기다리는 것은 waitgroup을 이용하는 것이 더 나은 경우가 많다.
6. 끝났음을 알리는 done 채널은 자료를 보내는 쪽에서 결정할 사항이 아니다. 자료를 보내는 쪽에서는 채널을 닫아서 자료가 끝났음을 알리는 것이 더 낫다.
7. done 채널에 자료를 보내서 신호를 주는 것보다, close(done)이 더 낫다.

---

# NginX Basics

	http {
	    server {
	        listen 8080;
	        root /home/hyuck/nginx; // root directory for static files
	
	        location /images {
	            // traffic to /images/filename will be served /home/hyuck/images/filename
	            root /home/hyuck/;
	        }
            //regex, anyfilename.jpg will match
            location ~ .jpg$ {
                return 403;
            } 
	    }
	}
	
	events { }
    
    $ nginx -s reload

위의 예시는 8080에 server를 연다. /home/hyuck/nginx의 static file을 제공하며, /images에 접근하면 /home/hyuck/images에서 제공한다. jpg로 끝나는 uri에 접근하면 403 error를 출력한다.

    server {
        listen 8888;
    
        location / { // localhost:8888/에 접근하는 traffic을 localhost:8080/으로 redirect한다.
            proxy_pass http://localhost:8080/;
        }
        location /img { // localhost:8888/img/something.png를 localhost:8080/image/something.png로 redirect한다.
            proxy_pass http://localhost:8080/images/;
        }
    }

    http {
        upstream allbackend {
            // ip_hash; // hash ip to decide where to send, handy for stateful applications
            server 127.0.0.1:2222;
            server 127.0.0.1:3333;
            server 127.0.0.1:4444; // scaled apps, load balanced in round-robin
        }
        upstream app1backend {
            server 127.0.0.1:2222;
        }
        upstream app2backend {
            server 127.0.0.1:3333;
        }
        server {
            listen 80; // need sudo privilege since 80 is reserved for system
            location / {
                proxy_pass http://allbackend/;
            }
            location /app1 {
                proxy_pass http://app1backend/;
            }
            location /app2 {
                proxy_pass http://app2backend/;
            }
            location /admin {
                return 403;
            }
        }

위의 예시는 layer 7 proxy 예제임.

    stream {
        upstream allbackend {
            server 127.0.0.1:2222;
            server 127.0.0.1:3333;
        }
        server {
            listen 80;
            proxy_pass allbackend; // smtp, websocket any tcp protocol will be allowed
        }
    }

위의 예시는 layer 4 proxy 예제임.

    server {
        listen 443 ssl;
    
        ssl_certificate /public_key;
        ssl_certificate_key /private_key;
    }

SSL Support

    server {
        ssl_protocols TLSv1.3;
    }
TLS 1.3 Support

    server {
        listen 443 ssl http2;
    }
HTTP2 Support

---

# GraphQL
GraphQL은 얼핏 봤을 때는 ORM의 일종이라고 생각할 수 있지만, GraphQL 자체에 Object-Relation mapping 기능이 지원되지 않고, 그 자체로 DB에 접속할 수 없다.\
GraphQL은 resolver function을 작성하며, MySQL 등 SQL System에 연결하여 사용한다.\
RestAPI 구조에서 흩어져있는 Endpoint를 하나의 Endpoint로 모으고, filter 기능을 통해서 back의 기능을 front에서 수행할 수 있도록 한 것이다.\
Client(PC, Mobile 등)의 성능이 높아지면서 SPA, Client-side rendering 등의 feature를 통해서 server에 집중되는 overhead를 front에 분배하는 기능이 점점 추가되는데, GraphQL 역시 그 일환이라고 볼 수 있다.

---

# Regex Example
```
	// Might be vscode specific
	match : \(([^(]+)\)\.strip\(\)\.replace\(' ', ''\).replace\('\\n', ''\).replace\('\\t', ''\)
	// Match anything that starts with ( and capture any text that is not ( and ends with ) and replace and so on
	replace : strip_all($1)
```

---

# Random Boolean Network
복잡한 기능을 다수의 간단한 노드의 네트워크로 표현하는 방식\
각 Node의 상태가 바뀔 때마다 Rule에 따라서 다른 Node의 상태를 변경한다.\
Node 사이의 Connection을 구성하는 Graph를 프로그래밍 Paradigm에 적용한 것이라 볼 수 있다.\
주로 Simulation 등 복잡한 Behaviour을 프로그램으로 Implement할 때 사용된다.\
Neural Net과 같이 Node 사이의 Connection에 따라 Result가 변화하므로 실험과 분석을 통해 결과를 얻는다.

---

# GopherCon2019 - How I Write HTTP Web Services...
1. Tiny main abstraction
```
	func main() {
	    if err := run(); err != nil {
	        fmt.Fprintf(os.Stderr, "%s\n", err)
	        os.Exit(1)
	    }
	}
	
	func run() error {
	    db, dbtidy, err := setupDatabase()
	    if err != nil {
	        return erros.Wrap(err, "setup database")
	    }
	    defer dbtidy()
	    srv := &server {
	        db: db,
	    }
	    // ...
	}
```

2. The server struct
```
type server struct {
	    db      *someDatabase
	    router  *someRouter
	    email   EmailSender
}
```

3. Constructor for server? - Don't setup dependencies here
```
	func newServer() *server {
	    s := &server{}
	    s.routes()
	    return s
	}
```

4. Make server an http.Handler - Implement ServeHTTP to tun your server into an http.Handler\
Use your server wherever you can use http.Handler\
Just pass execution to your router (don't hide your logic here)
```
	func (s *server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	    s.router.ServerHTTP(w, r)
	}
```

5. routes.go - one place for all routes
```
	package main
	
	func (s *server) routes() {
	    s.router.Get("/api/", s.handleAPI())
	    s.router.Get("/about/", s.handleAbout())
	    s.router.Get("/", s.handleIndex())
	}
```

6. Handlers hang off the server - Handlers are methods on the server, which gives them access to the dependencies via s\
careful not to have racing conditions as many handlers might be trying to access some resources in s
```
    func (s *server) handleSomething() http.HandlerFunc {
        //put some logic
    }
```

7. Naming handler methods - for autocomplete and docs purposes
```
handleTasksCreate
handleTasksDone
handleTasksGet

handleAuthLogin
handleAuthLogout
```

8. Return the handler - allows for handler-specific setup
```
    func (s *server) handleSomething() http.HandlerFunc {
        thing := prepareThing()
        return func(w http.ResponseWriter, r *http.Request) {
           // use thing
        }
    }
```

9. Take arguments for handler-specific dependencies
```
    func (s *server) handleGreeting(format string) http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            fmt.Fprintf(w, format, r.FormValue("name"))
        }
    }

    s.router.HandleFunc("/one", s.handleGreeting("Hello %s"))
    s.router.HandleFunc("/two", s.handleGreeting("Hola %s"))
```

10. Take arguments for handler-specific dependencies
```
    handleTemplate(template *template.Template) http.HandlerFunc
    
    handleRandomQuote(q QUoter, r *rand.Rand) http.HandlerFunc
    
    handleSendMagicLinkEmail(e EmailSender) http.HandlerFunc
```

11. Too big? Have many servers
```
    // people.go
    type serverPeople struct {
        db          *mydatabase
        emailSender EmailSender
    }

    // comments.go
    typeserverComments struct {
        db *mydatabase
    }
```

12. HandlerFunc over Handler - http.HandlerFunc implements http.Handler, which makes them interchangealbe
```
    func (s *server) handleSomething() http.HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {

        }
    }
```

13. Middleware are just Go functions - Take an http.HandlerFunc and return a new one\
Run code before/after the wrapped handler
```
func (s *server) adminOnly(h http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if !currentUser(r).IsAdmin {
            http.NotFound(w, r)
            return
        }
        h(w, r)
    }
}
```

14. Wire Middleware up in routes.go
```
	package main
	
	func (s *server) routes() {
	    s.router.Get("/api/", s.handleAPI())
	    s.router.Get("/about", s.handleAbout())
	    s.router.Get("/", s.handleIndex())
	    s.router.Get("/admin", s.adminOnly(s.handleAdminIndex()))
	}
```

15. Respond helper - Abstract responding and do the bare bones initially\
later make this more sophisticated(if needed)
```
    func (s *server) respond(w http.ResponseWriter, r *http.Request, data interface{}, status int) {
        w.WriteHEader(status)
        if data != nil {
            err := json.NewEncoder(w).Encode(data)
        }
    }
```

16. Decoding helper - Abstract decoding and do the bare bones initially
```
    func (s *server) decode(w http.ResponseWriter, r *http.Request, v interface{}) error {
        return json.NewDecoder(r.Body).Decode(v)
    }
```

17. Future proof helpers - Always take http.ResponseWriter and \*http.Request

18. Request and response data types
```
    func (s *server) handleGreet() http.HandlerFunc {
        type request struct {
            Name    string
        }
        type response struct {
            Greeting    string `json:"greeting"`
        }
        return func (w http.ResponseWriter, r *http.Request) {
            ...
        }
    }
```

19. Lazy setup with sync.Once - Perform expensive setup when the handler is first hit to improve startup time\
if the handler isn't called, the work is never done
```
    func (s *server) handleTemplate(files string...) http.HandlerFunc {
        var (
            init    sync.Once
            tpl     *template.Template
            tplerr  error
        )
        return func(w http.ResponseWriter, r *http.Request) {
            init.Do(func(){
                tpl, tplerr = template.ParseFiles(files...)
            })
            if tplerr != nil {
                http.Error(w, tplerr.Error(), http.StatusInternalServerError)
                return
            }
            // use tpl
        }
    }
```

20. net/http/httptest is your BFF
```
    func NewRequest(method, target string, body io.Reader)
        *http.Request

    type ResponseRecorder

    type Server
```

21. Server is testable - create a new server instance inside each unit test\
only set dependencies you need
```
    func TestHandleAbout(t *testing.T) {
        is := is.New(t)
        srv := newServer()
        db, cleanup := connectTestDatabase()
        defer cleanup()
        srv.db = db
        r := httptest.NewRequest("GET", "/about", nil)
        w := httptest.NewRecorder()
        srv.ServeHTTP(w, r)
        is.Equal(w.StatusCode, http.StatusOK)
    }
```

22. Test types help frame the test - request, response types are trapped inside the handler, we can make different types for our tests\
great storytelling opportunity
```
    func TestGreet(t *testing.T) {
        is := is.New(t)
        p := struct {
            Name string `json:"name"`
        }{
            Name: "Someone",
        }
        var buf bytes.Buffer
        err := json.NewEncoder(&buf).Encode(p)
        is.NoErr(err) // json.NewEncoder
        req := httptest.NewRequest(http.MethodPost, "/greet", &buf)
        //... more test code here
    }
```

23. Server is testable in two ways
```
    // test the whole stack (integration test)
    srv.ServeHTTP(w, r)

    // test just this handler (unit test)
    srv.handleGreet(w, r)
```

24. You can even make real HTTP requests
```
    func TestTips(t *testing.T) {
        h := newFakeRemoteService()
        srv := httptest.NewServer(h)
        defer srv.Close()
        resp, err := http.Get(srv.URL + "/api/tips")
    }
```

---

# Importing Packages for Side-effects
Go를 사용하다보면

```
	_ "github.com/example/something"
```

과 같이 pkg를 import하되 사용하지 않는 경우를 자주 보게된다.\
이것은 pakcage의 side-effect만을 사용하기 위함이다.

pkg가 직접 사용되지 않고 (pkg.Something처럼) 사용될 수 있는 경우는 2가지이다.

1. pkg-level variable 선언
2. pkg가 import되었을 때 call 되는 init func에 side-effects 주입

예를 들어 echo의 swagger middelware는 1, 2 모두를 사용한다.

```
	type s struct {}
	
	func init() {
		swag.Register(swag.Name, &s{})
	}
```
이것도 일종의 dependency injection이라고 볼 수 있을까?

---

# How to Efficiently Stream
Mobile에서 YouTube Vid를 사용하면 Response가 206 Partial Content HTTP Status를 전달하는 것을 볼 수 있다.\
videoplayback으로 시작하는 이 response가 실제로 video의 일부분에 대한 binary-encoded data이다.\
Edge Location의 CDN에 대한 response는 video가 (일정 부분에 한해서) 계속 전달되는 동안 계속 다운로드 되며 실시간 스트리밍 된다.\
HTTP3 (QUIC) 프로토콜을 사용하므로 Head of Line Blocking이 없다.\
반면에 Desktop Mode를 사용할 시, YouTube은 video와 audio를 분리해서 스트리밍한다.\
따라서 Payload를 최소화하여 안정적으로 스트림 할 수 있다.

---

# Go Mistakes
1. If something does not depend on the status of something, use Function. If it does, then use Method. A lot of people blindly uses Struct and Method having come from OOP backgrounds. Using methods should always mean that it might change the status of the datatype(class).
2. If the value(s) should be shared with functions or methods, use pointers. If not, use values, instead.
3. Thinking of errors as strings. Write pre-defined errors and use them.
4. Datastructres are not safe for concurrent acess. Yet, people will use it concurrently, should you share your code. To make them safe, use the Sync package or channel.

---

# GraphQL
GraphQL은 REST, RPC와 같이 API Design Specification이다.\
그렇다고 기존에 있는 REST API 서버를 없애고 GraphQL로 다시 구현할 필요 없이, 많은 endpoint중에 /graphql 처럼 하나의 GraphQL endpoint를 만들어 주는 것으로 충분하다.\
간단히 말해서 GraqhQL은 resource를 url이 아닌 query를 통해 표현하는 것이다.\
JOIN을 사용하지 않기 때문에 SQL Database와 궁합이 나쁠 것이라고 생각하는 경우가 많지만, Table을 entity로 매칭하기에 SQL과 GraphQL의 궁합은 나쁘지 않다.\
서버 개발자가 결정하는 것은 entity의 관계와 데이터를 어떻게 가져올 것이냐에 대한 것이다.\
REST에서 같은 데이터를 가져오기 위해서 여러 API를 작성하는 것과 반대로 graphql은 데이터를 요청하는 측에서 데이터의 depth를 정하므로 API 개발 load가 줄어든다.\
요청하는 데이터의 depth가 너무 깊어지는 것을 막기 위해서 query의 maxDepth를 설정하는 방식을 취하는 경우가 일반적이라고 한다.\
GraphQL을 사용하면서도 Join을 사용하기 위해서 join-monster 등의 라이브러리도 지원하고 있다.\


아래는 graphql-js에서 스키마 정의 예시이다.
```
var schema = new GraphQLSchema({
    query: new GraphQLObjectType({
        name: 'Character',
        fields: {
            name: {
                type: GraphQLString,
                resolve() {
                    return 'name';
                }
            },
            appearsIn: {
                type: GraphQLList(Episode),
                resolve() {
                    return [];
                }
            }
        }
    })
})
```

이를 graphql-tools를 사용하여 스키마를 더 명료하게 나타낼 수 있다.
```
// define type by raw string
const Comment = `
    type Comment {
        id: Int!
        message: String
        author: String
    }
`;
}

// get data from DB
const CommentResolver = () => {}

export const schema = makeExecutableSchema({
    Comment,
    CommentResolver,
});
```

GraphQL을 사용하면 일어나기 쉬운 1+N 문제를 1+1로 변환시키는 DataLoader의 사용이 필수적이다.\
NodeJS에서 이벤트 루프가 돌아가는 사이클 동안 들어온 id 기반 요청을 배치로 처리한 후 값을 돌려주는 방식으로 문제를 해결한다.\
Dataloader는 캐싱 기능을 가지고 있지만, Redis와 같은 in-memory storage와 같은 정의는 아니고, 한 요청이 처리되는 동안에 데이터를 캐싱한다는 뜻이다.\

REST의 GET이 아닌 모든 Method에 해당하는 데이터의 변형을 일으키는 요청을 Mutation이라 한다.\
mutation을 사용할 때 생길 수 있는 문제는 input type과 output type이 다른 것이다.\
input에 필요한 data와 output으로 나오는 data의 타입이 다른 건 당연하니까.\
그렇기 때문에 GraphQL에는 input type이 따로 존재하며, input type을 output type으로 함께 사용할 수 없도록 제약이 걸려있다.\
Header의 Content-Type은 application/json, application/graphql을 사용한다.\
application/json의 경우 아래 format을 따른다.
```
{
  "query": "...",
  "operationName": "...",
  "variables": { "myVariable": "someValue", ... }
}
```

반면에 application/graphql을 사용하면 아래 format을 따른다.
```
{
  human(id: "1000") {
    name
    height(unit: FOOT)
  }
} # id가 1000인 human entity의 이름과 FOOT 단위의 키를 뽑는다.
```

이 차이 때문에 variable을 사용하는 mutation 요청에서 application/json을 사용하면 graphql query를 직접 짜야되서 귀찮아진다.\
따라서 글쓴이는 Content-Type: application/json으로 통일될 것이라고 생각한다.

*항상 REST 방식으로만 개발했는데 GraphQL도 사용해보면 재밌을 것 같다.*

---

# GFS
Google File System
1. Stores 3 replicas for fail-over
2. Chunk size being 64 MB, which is much larger than 512 Bytes, the usual block size. The bigger the chunk size is, the less communication is needed between the client and the master server. Also, it reduces the metadata size on the master.
3. In case of a master crash, logs which are stored on the masters disk and replicated onto other replicas disks are used.
4. All metadata is stored in the master's memory. (Some are also stored in disk) By doing so, it is compact, fast, and simle.
5. By not keeping the chunk location information persisitently at the master, there is no need to sync the info the master has and the actual status. Which is a hard task in a large-scale distributed system.

Highly Available -> Replicas with Resource Scheduling
Multiple Levels, Types of Lock for efficiently managing multi-client environment

---

# Go internal server performance
한줄요약: 성능, 기능(SSL 인증 등)은 걱정하지 않아도 된다. 많은 회사들은 internal Go server를 사용한다. 하지만 DevOps 편의성, Cloud에서 설정을 위해서라면 Nginx, Apache를 사용할 수도 있다.
Go internal servers don't need another 'production' server to take requests and hand over to go servers. They can simply handle that many requests by themselves (Unless the framework's internal server completely mucked up building it)\
Many companies directly expose their Go servers to the Internet, even Google's download server is written in Go using net/http pkg.\
Yet there can be couple of reasons if you decided to put your go server behind a NginX server.\
First, DevOps people are more familiar with handling NginX config. Rather than being involved in the source code.\
Second, there might be some NginX, Apache (production) server specific config on your CSP or Infrastructure provider.\


---

# Autocomplete Implementation
자동 완성 기능을 구현해야한다.\
기존에 자동완성 기능을 지원했던 기능을 레퍼런스 삼아서 살펴보니 백에서는 모든 데이터를 전달하고, 프론트에서 (JQuery) Autocomplete 패키지를 사용하여 데이터를 필터링하는 방식으로 자동완성을 구현했다.\
당연하게도 백에서 전달하는 데이터가 클수록 프론트에서 자동완성에 사용되는 오버헤드가 커진다. 만약 데이터가 어느 정도 이상 크다면 서버의 네트워크 throughput도 생각해봐야 할 수 도 있다.\
프론트에서 필터링을 통해서 자동 완성을 구현하는 대부분의 레퍼런스를 제외하면, 나머지는 SQL로 ㄱ으로 시작하는지, 혹은 가와 나 사이에 글자가 있는지를 체크하는 레퍼런스가 대부분이다.\
문제는 내가 자동 완성해야할 데이터는 한글, 띄어쓰기(이것도 포함된 레퍼런스는 꽤 많다.), 알파벳과 어쩌면 기호도 포함될 것이라는 점이다.\
이런 모든 경우의 수를 레퍼런스에서 알려주는 방식대로하면 SQL Function이 너무 복잡해질 것 같고 (내가 Query 전문가가 아닌 게 큰 이유겠지만, 난 왠만하면 DB에서 뭔가 복잡한 일을 하는 걸 별로 안 좋아한다.), 오버헤드도 작지 않을 것 같다.\
얼마 전에는 LIKE 때문에 DB에 과부하가 걸렸던 적도 있으니까..\
그렇다면 Micro Service를 하나 만들어서 하트빝을 통해서 타겟 테이블의 데이터를 최신 데이터로 유지, 그 데이터를 해체해서 메모리에 보관하다가(or json으로?) 정규식 + a로 결과를 return하는게 좋지 않을까 생각한다.\
물론 여기에 사용할 언어는 Go가 좋을 것 같다. 퍼포먼스가 좋고, 데이터 정합성 체크와 서버 + a 역할을 동시에 처리한다. 용도가 딱 맞는 것 같아서..\
구현하게 된다면 구현의 어려움, 알고리즘 구현에 대해서 기록하겠다(아마도 b-tree에 단어 분리, 초성 체크, 초성이 중간에 끼었을 때 처리 그런게 어렵겠지)

18/DEC/2020
당연히 B Tree가 아니다. B Tree로 하는 방법이 있을 수도 있겠지만, a 글자 다음에 올 수 있는 글자는 특수 문자, 알파벳 등 수천가지가 넘을 수 있다. 따라서 가지를 치는 Tree 구조는 맞지만 Binary는 아니다. 훨씬 더 많은 가지를 칠 수 있다.\
이런 구조를 Prefix Tree라고 한다.\
Prefix Tree를 써야겠구나하고 reference없이 혼자 만들기 시작했는데, 단어 추가, 검색을 진행하던 중에 하나 더 깨달은 점이 있다.\
지금 내가 계획없이 그냥 진행한 PrefixTree 구조를 간단히 para-표기하면 아래와 같다.
```
type PrefixTreeNode struct {
    Syllable        rune
    SyllableType    int
    Nexts           []*PrefixTreeNode
}
```
Syllable은 한글일 경우 초성, 중성, 종성을 분리해서 저장하며, SyllableType이 한글(초,중,종), 영어, 그외(특수문자+숫자 등)를 분간한다. Nexts에는 현재 Node를 prefix로 가지는 다른 Node들의 Pointer를 저장한다.\

하지만 Node가 LeafNode가 아닐때에는 이 Node가 단어의 끝인지, 다음 Node의 Prefix로만 존재하는지 알 수 있는 방법이 없다.\
Prefix Tree의 reference를 찾아보니 index를 사용하는 경우가 있다.\
단어가 끝나는 지점에서 index를 부여해서 index가 있는 부분은 중간일 수도, 단어의 끝일 수도 있는 것을 선언하는 것이다.\
하지만 왜 하필 index일까? 메모리를 아끼기위해서는 단어의 끝임을 알리는 struct {}{} 혹은 bool이 더 나을텐데?\
ChildNode를 따라 아래까지 더 추적하지 않아도 해당 prefix를 가진 Node에만 도달하면, 어떤 단어를 자동 완성할지를 알 수 있는 것이다. 단어의 길이가 길수록 속도가 향상될 것이며, 코드가 간단해진다. 긴 단어가 많을수록 매 Node에 같은 []int를 저장시켜야 하므로 메모리를 더 많이 사용하지만 앞의 장점과 trade-off라고 생각한다면 훨씬 더 나은 선택이다.

---

# make and new in Go
```
The built-in function make takes a type T, which must be a slice, map or channel type, optionally followed by a type-specific list of expressions.
It returns a value of type T (not *T).
```
```
Although make creates generic slice, map, and channel values, they are still just regular values; make does not return pointer values.

If new was removed in favour make, how would you construct a pointer to an initialised value ?

Using new to construct a pointer to a slice, map, or channel zero value works today and is consistent with the behaviour of new.

For the confusion they may cause, make and new are consistent

make only makes slices, maps, and channels,
new only returns pointers to initialised memory.
```
사실상 new를 사용하는 경우는 거의 없다. 굳이 사용한다면 빈 구조체를 initialise하고 그에 대한 포인터를 만드는 용도?\
하지만 &my\_struct{}가 더 명시적이지 않을까? 또 built-in type의 pointer로 사용한다고 하더라도 

```
ptr := new(int) // 이렇게 하고나서 다시 ptr = &val 을 한다? 같은 일을 두 번할 뿐

var ptr *int    // 같은 방식을 취할 거라면 이게 더 보기 쉽다.

ptr := &val     // 이게 가장 많이 사용될테고
```

오랜만에 new를 코드에 사용하면서, 뭔가 헷갈리기도 하고 잘못한 것 같은 느낌이 들어서 찾아봤다.\
일할 땐 Python, 개인적으로는 Go, 알고리즘은 C++, Go, 가끔씩 JS도 디버그하고.. 하다보니 우연히 튀어나온 new이지만, Go에 한해서는 용도가 매우 한정되있다고 생각한다.

---

# Package in Go
Go는 기본적으로 Relative Import를 지원하지 않는다.\
Python으로 치면 from ..pkg.something import some\_func 같은.\
Go Path에 pkg를 생성하고 사용하는 방식은 go mod 이후 거의 deprecate되는 추세라고 한다.

Go의 package는 간단하게 말하면 디렉토리를 뜻한다.\
module을 이루는 디렉토리에서 시작해서 그 하위 디렉토리는 모두 하나의 package(sub-package?)라고 볼 수 있으며, package의 이름은 디렉토리와 일치하지 않아도 된다.(하지만 그렇게 하면 alias를 사용하지 않을 경우 상당히 사용하기가 힘들 것이다.)\
하지만 한 package에서, 즉 한 디렉토리 내에서 모든 파일은 하나의 package를 가리켜야한다.\
```
github.com/woodchuckchoi/something/
| main.go - package main
| something.go - package something
...
```
이런 식으로는 사용할 수 없다는 것이다.\
내 프로젝트는 package와 main을 같이 사용하는 경우, 즉 패키지 안에 엔트리포인트도 같이 있는 경우 binary라는 디렉토리를 따로 두고 여기에 main package를 넣어서 사용하기도 한다.\
일반적으로 package를 사용할 때 base directory에 위치한 package를 사용하는 경우가 많으니까 이 방식이 맞을수도, 아니면 utility package에는 당연히 main package를 넣지 않을 수도 있다.\
지금 내 경우에는 package를 혼자 만들고 있으니까 이런 식으로 사용하는 것이고.

Go의 package managing 방식은 github, bitbucket 등 repository를 이용하는 방식이기 때문에 public이 아닌 package를 사용하기 위해서는 몇가지 설정이 필요하다.
```
git config --global url.git@github.com:.insteadOf https://github.com // https 방식을 ssh 방식으로 바꿔준다. ssh key가 등록되어 있다면 identity check을 위한 prompt가 생략되므로.

go env -w GOPRIVATE=github.com/<OrgName>/\* // proxy, checksum database를 사용하지 않고 repository에 접근한다.
// eg) go env -w GOPRIVATE=github.com/woodchuckchoi/*,bitbucket.com/user/* 같이 comma-seperated string이다.
```

package의 versioning은 다음 표기법을 따른다. v[Major].[Minor].[Patch]\
go get -u (upgrade)를 통해서 upgrade 가능하다.\
major version change는 go.mod의 module을 변경함으로써 진행되고, minor version change는 git의 tag를 통해서 설정한다.\
go.mod의 major version과 git tag의 semantic version의 major version이 일치해야한다.

---

# Concurrency and Go
Thread 사이에는 parent/child relationship이 존재하지 않는다. 다시 말해 A thread가 B thread를 생성하고 A thread가 종료되더라도 B thread가 종료되지는 않는다.\
하지만 예외적으로 A thread가 main thread 일 때, 그리고 어떤 thread가 exit system call을 호출 했을 때 다른 thread에 영향을 끼칠 수 있다. Process의 Main함수를 담당하는 Main thread가 exit하면 process도 exit하고 process에 속한 thread 모두 exit한다.

Goroutine은 thread지만 여러 core의 resource를 활용할 수 있다.\
이것은 Go가 clone system call을 사용해서 goroutine을 관리하기 때문이다. Clone은 child process가 parent process의 address를 그대로 사용하게 함으로써 memory는 공유하면서 CPU core는 각각 사용할 수 있도록 한다.

Goroutine은 아래와 같은 형태를 띈다.
```
OS Process(P) - OS thread(M) - Goroutine(G)
```
goroutine을 생성할 경우 Go는 설정에 따라 여러 Process를 생성한다.\
생성된 idle Process 중 process를 선택해서 thread(M)를 생성한다.\
생성된 M에 goroutine(G)를 생성한다.

Go에서 동시성을 구현할때는 단순화를 목표로 하고 가능하면 채널을 사용한다. 고루틴은 무한정 쓸 수 있는 자원처럼 다룬다.

모든 Go 프로그램에는 적어도 하나의 Goroutine이 있다. Main Goroutine (Main Thread처럼)가 그것이다.\
Goroutine은 Coroutine이라 불리는 높은 수준의 추상화다.\
Coroutine은 동시에 실행되는 (병렬이 아닐 수 있다.) 서브루틴으로 인터럽트가 불가능하다. 하지만 중단하거나 재진입할 수 있는 여러 Point를 가진다.\
Goroutine은 중단이나 재진입 포인트를 정의하지 않고, Go runtime이 goroutine을 관리한다.\
Goroutine을 호스팅하는 Go의 메커니즘은 M:N 스케줄러로, M개의 그린스레드를 N개의 OS 스레드에 매핑한다.\
Goroutine은 스레드에 스케쥴링 된다. 사용가능한 그린스레드보다 더 많은 Goroutine이 있다면 스케줄러는 사용 가능한 스레드들에게 Goroutine을 분배하고, 분배된 Goroutine이 대기 상태가 되면 다른 Goroutine이 실행되도록 한다.

Goroutine은 약 2kb의 메모리를 차지하며, 컨텍스트 스위칭에 사용되는 비용도 OS의 Thread보다 훨씬 저렴하므로 동시성 프로그래밍에 알맞다.

Cond는 고루틴들이 대기하거나, 어떤 이벤트의 발생을 알리는 rendezvous point이다.\
여기서 이벤트는 복수의 고루틴 사이에서 어떤 사실이 발생했다는 사실만을 전달하는 임의의 신호이다.(마치 chan <- struct{} {}와 같다)\
Cond를 사용하지 않는 가장 단순한 접근 방법은 무한루프일 것이다.

```
for conditionTrue() == false {
}
```

하지만 위의 방법은 한 개 코어의 모든 사이클을 소모한다. 이를 개선하면 아래와 같다.

```
for conditionTrue() == false {
    time.Sleep(time.Millisecond)
}
```

위 방법 역시 sleep을 얼마나 할 것인가에 따라 낭비가 생긴다.\
여기서 필요한 '고루틴이 신호를 받을 때까지 슬립하고 자신의 상태를 확인할 수 있는 방법이 Cond Type이다.\
Cond를 사용하면 아래와 같이 개선할 수 있다.

```
// 이 코드는 무시하자
c := sync.NewCond(&sync.Mutex{})
c.L.Lock()
for conditionTrue() == false {
    c.Wait()
}
c.L.Unlock()
```

위 방법은 현재 고루틴을 일시 중단해서 다른 고루틴들이 OS 스레드에서 실행될 수 있도록 하기 때문에 resource 관리 측면에서 훨씬 더 효율적이다.\
Wait()이 호출되면 c.L.Unlock()을 실행한다. Wait()이 종료될때는 c.L.Lock()을 실행한다.

Signal()은 Cond Type이 Wait 호출에 멈추는 고루틴에게 조건이 발생했음을 알리는 두 가지 메소드(Broadcast, Signal) 중 하나이다. Signal은 FIFO의 가장 오래된 고루틴에게 신호를 알려주고, Broadcast는 모든 고루틴에게 신호를 보낸다.\
chan을 사용하면 모든 고루틴에게 신호를 보내는게 어렵지 않지만, 반복적으로 호출하는 동작을 간단하게 구현해놨다는 점, 그리고 채널을 사용하는 것보다 성능이 좋다는 점이 Cond와 Broadcast의 사용 이유일 것이다.



---

# Bridge Channel
<- <- chan interface{} 와 같은 형태를 bridge 채널이라고 부른다.\
channel의 stream과 같은 형태이다.\
bridging의 use case는 아래와 같다.

```
bridge := func(done <-chan interface{}, chanStream <-chan <-chan interface{}) <-chan interface{} {
    valStream := make(chan interface{})
    go func() {
        defer close(valStream)
        for {
            var stream <-chan interface{}
            select {
            case maybeStream, ok := <-chanStream:
                if !ok {
                    return
                }
                stream = maybeStream
            case <-done:
                return
            }
            for val := range orDone(done, stream) {
                select {
                    case valStream <- val:
                    case <-done:
                }
            }
        }
    }()
    return valStream
}
```
