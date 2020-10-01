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
