# HTTP/1.1
Application 레이어에서 정의된 프로토콜\
연결 상태를 유지하지 않음(비연결성)/TCP는 연결형이지만 TCP위에 구성된 HTTP/1.1은 아니다.\
HTTP/1.1의 구성
* Header
	* General Header (Cache, No-cache, etc)
	* Request/Response Header (Host, User)
	* Entity Header (Content-Type)
* Blank Line
* Body

예시

	PUT /create_page HTTP/1.1
	HOST: localhost:8000
	Connection: keep-alive
	Upgrade-Insecure-Requests: 1
	Content-Type: text/html
	Content-Length: 345

	Body line 1
	Body line 2

---

# REST
Resource의 이름이나 구분을 통해서 Resource에 대한 정보를 주고 받는 개발 패러다임\
URI에 HTTP Method로 구분되는 Request를 보내고 그에 해당되는 Response 수신\
특징
* Stateless - 상태에 구애받지 않고 들어오는 요청만 수행한다.
* Cacheable - GET과 같은 Method에 한해서 expires 헤더를 설정하면 브라우저는 caching
* Layered System - API Response 뿐만 아니라 Authentication 등의 계층 추가 용이\
*RPC의 경우 Resource의 이름/구분이 아닌 Function에 대해 Request를 보내는 차이가 있을 뿐, 어느 패러다임이 더 우수/열등하다고 할 수 없다.*

---

# gRPC
Protocol Buffer라는 Message라는 미리 설정된 (Static) Bytes 형식으로 Payload를 encoding하여 역시 미리 설정된 Service라는 RPC Function을 향해 HTTP/2 환경에서 통신하는 RPC 형태의 프레임워크\
통신 순서
* Client가 Stub Method (Parameter와 Return 타입, Service명)를 Call하면 Server는 Client의 Metadata를 전송받고, 바로 Metadata를 전송할지 Request Body를 전송받고 Metadata를 전송할지 결정한다.
* Client의 Request를 전송받고 로직을 실행한 뒤 서버는 Trailing Metadata와 함께 Response를 전달한다.
* gRPC Call이 발생하면 gRPC Client는 Server와의 Connection을 생성한다. 다수의 Connection을 생성하여 보틀넥의 피해를 줄이는 HTTP와는 다르게 HTTP/2에서는 한 개의 Connection에 사실상 무한한 bi-directional Stream을 생성하여 Multiplexing이 가능하다.

---

# HTTP/2
TCP/IP Layer 중 Application Layer에 Binary Framing Layer가 추가되어 아래의 기능이 HTTP/1.1보다 향상되었다.
* Header 압축을 통해서 latency 줄임
* 한 개의 커넥션에서 Concurrent한 데이터 교환 가능
* 기본 단위는 Frame으로 Header와 Data Frame은 HTTP/1.1의 Request, Response에 해당하며, 이를 제외한 Settings 등의 Frame은 HTTP/2의 Feature를 담당한다.
* Stream은 양방향으로 통신하기때문에, Blocked, Stalled로 인해서 Progress에 영향을 끼칠 염려가 적다.
* Flow Control은 각 Stream이 서로에게 영향을 끼치지 않도록 제어하는 역할을 한다. 예를 들어 의존성이 있는 스트림의 순서 정렬, 중요도에 의한 리소스 배정과 같은 것이다.
* Prioritisation은 Headers Frame의 priority attribute에 따라 Resource 점유에 우선순위를 두는 것이다.
* Multiplexing: Multiple different server requests are allowed simultaneously, on the same connection. With HTTP/1.1, each additional requests for assets would have to wait until the previous transfer in the queue completed. This decreases complexity in development, not necessitating things like asset bundling to decrease to number of server requests.\ 
한 스트림 내에서 다수의 Request를 Frame으로 분할하여 다수의 Request/Response를 동시에 처리\
\
대부분의 브라우저는 여러 Request를 보내야 할 때, 여러 Connection을 만들어서 각 Request 사이의 Latency를 줄인다. 하지만 Connection이 많아지면 Server의 Overhead가 커진다는 단점이 있다. 그렇기 때문에 HTTP/2가 생겼다.\
HTTP/2 역시 TCP를 기반으로 하기 때문에, Packet 레벨에서 문제가 생겨서 이 데이터를 Parsing 할 수 없다면 Blocking이 생기게 된다.

"""
GET Req packet 1 O
Get Req packet 2 O
Get Req packet 3 X // Packet 실종, Retransmit X
POST Req packet 1 O
POST Req packet 2 O
POST Req packet 3 O
// HTTP2에서 위와 같이 Multiplex가 이루어졌다면, POST Request도 멈춰버리게된다.
"""

## Frame
프레임은 HTTP의 Request와 Response를 대체하는 HTTP/2의 통신 단위이다. 각 프레임은 TCP/IP 네트워크 모델의 Application Layer에 추가된 HTTP/2 Binary Framing Layer에서 Binary로 인코딩된다.\
이 방법의 장점은 Header를 Body와 같은 독립적인 프레임으로 취급하면서, 헤더 압축이 가능해졌다는 점이다. HTTP/1.1에서 헤더와 바디는 한 요청을 구성하면서, 압축이 되지 않았기 때문에 각 요청의 크기가 컸다. 이는 TCP Protocol의 Slow Start 기능과 만나 HTTP/1.1에서 페이지 로드 속도가 심각하게 느려지는 원인이 됐다.\
TCP의 Slow Start는 Sender가 아주 작은 패킷을 보내고, Receiver가 이것을 받아들여 ACK 신호를 보내면 보내는 패킷의 크기를 조금 더 키우는 방식으로 패킷을 얼마나 크게 보낼 수 있는가에대한 지침을 제공한다.\
네트워크 상의 각 호스트가 같은 크기의 버퍼를 제공하지 않기 때문에 고안된 방식이지만, 요청이 헤더와 바디를 모두 포함하며, 압축 기능도 제공하지 않는 HTTP/1.1 스펙에서는 요청 응답 시간을 느리게 하는 주범이 되었다.
## Stream
스트림은 어떠한 실체가 있지 않은, Bi-Directional한 Frame의 Identifier이다. Stream의 개수에는 제한이 없어서 사실상 무한정으로 생성할 수 있다.\
여기에서 Stream이 Bi-directional하다는 뜻은 요청에 대한 응답이 같은 stream identifier를 사용하기 때문에 양방향성을 띈다는 뜻이다.\
HTTP/1.1에서 어떠한 Request의 비용이 비쌀 경우 다른 Request는 새로운 Connection을 생성하여 처리했지만, Stream은 한 Connection 내에서 무한정으로 생성할 수 있으므로 Stream 생성에 대한 부담이 적다.\
모든 Frame은 Session내에 Unique한 Stream ID를 갖는데, 충돌을 피하기 위해서 Client가 Push하는 Frame은 홀수, Server가 Push하는 Frame은 짝수 Stream ID를 갖는다.\
서로 다른 Stream ID를 가지더라도, 한 뭉치로 뭉쳐서 보내질 수 있다. Frame의 Header는 최소한 Stream ID 헤더를 항상 가지고 있으므로, 이를 기반으로 어떤 Stream에 속하는지 알 수 있다.

---

# JWT(Json Web Token)
JSON Object를 Hash를 통해서 안전하게 전달하는 기술\
Header, Payload, Signature로 구성된 JSON Object를 Base64형태로 치환하여 전달
* Header에는 alg, typ(jwt)
* Payload에는 데이터
* Signature는 Header와 Payload를 Base64 encoding 후 private key(salt)를 이용하여 alg로 암호화
수신자는 public key를 사용하여 전달자의 정체를 알 수 있다.

---

# TCP/IP - OSI
TCP/IP와 OSI는 모두 네트워크의 작동 방식을 설명하는 모델이다.\
OSI는 네트워크의 각 단계를 7단계로 나눈 반면에, TCP/IP는 4단계로 나누어 설명한다. 계층을 나눔으로써 각 단계의 사양이 변경되었을 때, 구성을 변경하기 쉽다는 장점이 있다.\
TCP/IP의 레이어
* Application은 유저에게 제공되는 Application의 통신을 결정하는 레이어. FTP(파일 전송), HTTP, POP3(메일)등의 응용 레벨의 프로토콜을 제공한다.
* Transport은 네트워크에 접속된 컴퓨터 사이의 데이터 흐름을 Application Layer에 제공하는 역할을 한다. TCP와 UDP라는 두 가지 프로토콜을 가진다.
* Network는 네트워크 상에서 패킷의 이동, 어떤 경로를 통해 패킷을 전달할 것인가를 다룬다. 공유기 - 라우터 - 이더넷 - 파이버 - 이더넷 - 서버와 같은 특정 경로.
* Network Interface는 네트워크에 접속하는 하드웨어 계층을 담당한다.

IP(Network Layer)는 패킷의 배송을 담당한다. 목적지의 위치 (IP와 MAC 주소)를 참조하여 그 다음 라우터로 데이터를 전송한다.\
TCP(Transport Layer)는 신뢰성을 담당한다. 데이터를 TCP Segment라고 불리는 Packet으로 조각내고, 연결이 설정되었는지를 3-Way Handshake을 통해서 확인한다.

1. Sender는 Receiver에 'SYN' 신호와 함께 Packet을 전달한다.
2. Receiver는 Packet을 수신하고 'SYN/ACK' 신호를 Sender에 전달하여, 패킷을 수신했다고 알린다.
3. Sender는 Receiver에게 'ACK' 신호를 전달하여 'SYN/ACK' 신호를 수신했다고 알린다.

TCP/IP로 보는 HTTP 통신의 순서는 아래와 같다.
1. 클라이언트의 Application Layer에서 어느 웹페이지를 보고 싶다라는 HTTP Request를 생성한다.
2. Transport Layer에서는 Application Layer의 Request를 통신하기 쉽도록 Packet으로 조각내어 안내 번호와 포트 번호를 붙여 Network Layer에 전달한다.
3. Network Layer는 수신지의 고유 주소인 MAC 주소를 추가하여 Network Interface Layer로 전달한다. Network Interface Layer는 통신의 하드웨어를 담당하여 데이터를 전송한다.
4. 수신하는 측(Server)는 위의 과정을 역순으로 실행하여 데이터를 수신한다.

*IP 주소는 각 노드에 부여된 주소를 뜻하며, MAC주소는 각 네트워크 카드에 할당된 고유 주소를 뜻한다. IP주소는 변경 가능하지만, MAC주소는 변경할 수 없다*.\
*DNS는 Application에서 Domain Name의 실제 주소인 IP를 확인 할 수 있도록 돕는 역할을 한다*.

Request를 수신하면 Receiver는 ACK를 기다린다. Sender의 TCP는 ACK가 올 때까지 일정 시간을 기다리다가 ACK가 도착하지 않은채 타이머가 울리면 패킷을 다시 보낸다.(Retransmit)

OSI의 레이어
* Application - 사용자가 Interact하는 Layer
* Presentation - OS가 Application Layer의 데이터를 받아서 인코딩, 암호화 등을 담당하는 Layer
* Session - Connection의 일부인 Session을 구축하는 Layer
* Transport - 데이터를 Packet으로 자르고, 어떤 크기의 Packet으로 데이터 통신을 할 것인지 담당하는 Layer, Connection을 구축한다.
* Network - 노드 사이의 논리적인 경로를 결정하는 Layer
* Network Link - 하드웨어 + 소프트웨어적으로 데이터 운송을 담당하는 Layer
* Physical - 하드웨어 레벨에서 데이터 운송을 담당하는 Layer

---

# HTTPS
* 대칭키 방식
인터넷 사이트는 CA에 공개키를 제공한다.\
CA는 CA의 개인키로 인터넷 사이트의 정보를 암호화하여 인증서를 발급한 후, 자신의 공개키를 웹브라우저에 제공한다.\
사용자가 인터넷 사이트에 접속하면 인증서를 웹 브라우저에 보내고, 사용자는 CA의 공개키로 인증서를 복호화하여 사이트의 정보와 공개키를 받는다.\
공개키로 대칭키를 암호화하여 사이트에 보낸다.\
사이트는 개인키로 데이터를 복호화하여 대칭키를 생성하고, 이제 대칭키를 통해서 통신한다.\
세션이 종료되면 대칭키를 폐기한다.\
*대칭키는 매번 사용할 때마다 다른 키가 생성되므로 비교적 안전하고, 공개키보다 속도가 빠르다는 장점도 있다.*

HTTPS를 사용할 경우 암호화, 복호화에 시간이 소요되므로 속도가 느려지게 되며, CA의 인증서를 생성하고 유지하는데 비용이 필요하다.\
암호화된 데이터를 캐싱할 수 없기 때문에 이를 위한 별도의 스텝이 필요하다.\
특정 프레임워크에서 지원하지 않는다면 기존에 존재하는 URI를 HTTPS 프로토콜로 변경해야한다.\

* 공개키-개인키 방식
TLS(Transport Layer Security)를 사용한 HTTP 통신 암호화 기법이다. SSL(Secure Socket Layer)는 2015년 Deprecated.\
암호화는 Public-Private Key를 통해서 진행된다. Public으로 암호화 된 데이터는 Private으로만 복호화 할 수 있으며, Private으로 암호화 된 데이터는 Public으로 복호화 할 수 있다.\
이 중 Public Key를 신뢰할 수 있는 공개키 저장소(CA)에 등록한다. Server는 Server만 알고있는 Private Key를 소유하고 있는다.\
Client에서 Request는CA의 Public Key를 통해서 암호화 된다. 이 HTTPS Request를 받으면 Server는 Private Key를 통해서 암호화된 데이터를 복호화 한다.\
Server는 Request에 해당하는 응답을 Private Key로 암호화하여 Client에 보낸다.\
Response를 받은 Client는 Public Key를 이용하여 암호화된 HTTPS 데이터를 해독한다.\
*Public Key는 누구나 접근할 수 있으므로 보안상에 의미가 없다고 생각할 수 있지만, Public Key를 통해서 Response를 해독할 수 있다는 말은 Private Key로 암호화 되었다는 뜻이고, 이는 Server가 해당 Response를 보냈다는 것을 보장한다*.

---

# TCP/UDP
TCP/IP 네트워크 모델의 Transport Layer에서 지원하는 프로토콜이다.
* TCP는 가상 회선 방식을 제공하여 논리적인 경로를 배정한다. 연결형 서비스이며, Packet이 전달되었는지를 확인하고, 전달이 되지 않았다면 다시 전달 하는 등 신뢰성을 보장하지만, 연결 설정, 해제에 자원이 필요하여 UDP에 비해 속도가 느리다.
* UDP는 논리적인 경로를 설정하지 않기 때문에, 전달하는 각각의 Packet은 다른 경로로 전달된다. 비연결형 서비스이기 때문에 연결을 설정, 해제하는 과정이 없다. 신뢰성보다 속도가 더 중요한 Streaming 서비스에 주로 사용된다.

---

# Socket 통신
Socket 통신은 Request에 대한 Response 응답 후 연결을 끊는 HTTP 통신과 달리 Server와 Client가 특정 Port를 통해 연결을 유지하여 실시간으로 양방향 통신이 가능한 통신 방식이다.\
HTTP는 Client만 Request를 보내고 Server는 이에 응답하는데 반해 Socket 통신은 Server가 Client에게로 먼저 데이터를 보낼 수 있으며, 연결을 해제하기 전까지 계속 연결을 유지하는 연결지향형 통신이기 때문에 실시간 통신이 필요한 게임, 채팅 등에 주로 사용된다.

---

# Forward VS Redirect
* Forward는 URI에 전달된 Request를 서버가 Target URI에 전달한다. 전달받은 URI에서 버는 클라이언트에게 Response를 리턴한다.
* Redirect는 서버가 클라이언트에게 새로운 URI로 Request를 보내라는 신호를 전달한다. 클라이언트는 새로운 URI에 새로운 Request를 보낸다.\
*새로고침 등을 했을 때, 같은 데이터를 보내는 문제를 피하기 위해서 Redirect를 사용한다. 하지만 조회 등의 간단한 기능에는 Forward를 사용해도 된다*.

---

# A Record & CNAME
A 레코드는 DNS와 IPV4를 연결하는 방식이다. 이에 반해 CNAME은 DNS에 대한 또 다른 DNS라고 볼 수 있다. 
	someURI.abc -> properURI.com
CNAME을 사용하여 DNS나 IP가 바뀔 때마다 이에 맞춰 다른 사양 역시 변경해야되는 일을 피할 수 있다.

---

# Session을 Database를 사용하지 않고 유지하기
HTTP 프로토콜은 연결의 상태를 유지하는 기능이 없다.\
예를 들어 사용자가 로그인을 했다고 해도, 그 정보를 지속적으로 알고 있을 수 없다.\
따라서 사용자가 서버에 접근할 때 사용자를 식별할 수 있는 정보를 URL 파라미터로 전달하거나, 브라우저에 쿠키를 심어서 사용자의 상태를 기억하게 할 수 있다.\
물론 위의 방법은 파라미터 및 쿠키를 통해서 민감한 데이터에 접근할 수 있으므로 보안상의 이유로 Deprecate된 옛날 방식이므로, 최근에는 로그인했을 때, 의미가 없는 문자열(UUID)를 쿠키에 저장하게 하고 데이터베이스를 통해서 해당 문자열과 아이디 등의 정보를 조합하여 세션이 만료되었는지, 아직 효력이 있는지를 확인한다.\
혹은 서버의 앞단에 Gateway Server를 구성하여 세션을 관리하도록한다.

---

# 다수의 클라이언트가 어떻게 한 서버의 한 포트에 접속할 수 있을까?
Port를 사용한다는 뜻은 패킷의 헤더에 Destination Port를 명시했을 뿐이다.\
Stateless Protocol(UDP)를 사용할 때는 문제가 없다. 왜냐하면 Connection을 설정, 해제하지 않으므로 연결이 겹치는 상황이 생기지 않으니까.\
Stateful Protocol(TCP)를 사용할 때, Connection은 (Source IP, Source Port, Destination IP, Destination Port) 형태의 튜플로 구성된다.\ 
따라서 서로 다른 클라이언트가 동일한 서버에 접속한다고 Connection이 충돌하는 경우는 없다.\
\
만약 같은 클라이언트 or 서로 다른 클라이언트가 NAT이나 공유기를 통해서 한 서버에 접속한다해도, 서버가 인식하는 Source Port는 NAT Gateway나 공유기의 서로 다른  Port가 되므로 Connection은 구분이 가능하다.\
*만약에 Connection의 Source IP, Source PORT가 같다면 이 Connection들은 같은 Connection으로 인식된다.*

---

# Session VS Connection
Session은 Connection의 Superset이다.\
Connection은 (Source IP, Source Port, Destination IP, Destination Port) 형태로 이루어진 튜플이지만, Session은 App Control, Identity 등의 정보를 포함하고 있다.\
세션 유지는 로그인 혹은 상태 유지 시에 클라이언트의 쿠키에 의미 없는 데이터를 주고, 이를 서버 사이드의 데이터베이스와 비교하는 방식으로 작동한다.

---

# Load Balancing Techniques
* Round Robin - 연결되어 있는 노드에 순서대로 돌아가면서 트래픽을 전달하는 방식
* Weighted Round Robin - 각각의 노드에 Weight를 주어 우선 순위를 배정하는 것
* Least Connection - 현재 가장 적은 수의 커넥션이 연결되어 있는 노드에 트래픽 전달
* Weighted Least Connection - Least Connection 방식에 Weight 적용
* Resource Based - 노드에 서비스를 설치하여 현재 사용 중인 리소스에 따라서 트래픽을 배정한다.

---

# CORS 에러

CORS(Cross-Origin Resource Sharing) 정책을 위반하면 발생하는 에러.\
https://www.google.com/path?sort=asc&page=1#fragment 와 같은 URI가 있을 때, Origin은 https://www.google.com/path, Protocol, Host, Port를 합친 값이다.\
CORS는 같은 Origin에서만 리소스를 공유할 수 있다는 보안 정책이다.\
하지만 다른 Origin의 리소스를 가져와서 사용하는 것이 기본적으로 HTML, 웹이기 때문에 CORS를 따른다면 다른 Origin의 리소스를 가져와서 사용하는 것을 용납한다.\
*CORS가 없다면 CSRF나 XSS와 같은 공격에 취약해진다.*
Origin이 같다고 판단하는 로직은 Protocol, Host, Port의 값이 일치하는가?이다.\
*https://my-site.com 이라는 웹 사이트가 있을 때, Origin을 비교해보면*
	같은 Origin
	https://my-site.com/hello
	https://my-site.com/hello?query=val
	https://user:password@my-site.com
	
	다른 Origin
	http://my-site.com
	https://my-site.co.kr
	https://something.my-site.com

	브라우저에 따라 다름
	https://my-site.com:443 Origin에 포트가 명시되지 않았다면 브라우저마다 다른 로직을 사용하여 비교한다.

CORS는 브라우저에서 구현되기 때문에, 브라우저를 통하지 않고 통신을 할 때는 해당 정책이 적용되지 않는다.\
또한 서버 사이드에서는 정상적으로 Response를 줬다고 출력되기 때문에, CORS를 알지 못하면 에러 처리가 힘들다.\

	브라우저는 Request 헤더의 Origin 필드에 해당 Origin을 넣어 보낸다.
	Origin: https://my-site.com

	서버는 Response 헤더의 Access-Control-Allow-Origin 필드에 해당 리소스에 접근을 허용할 출처를 넣어서 응답한다.
	예를 들어 https://my-site.com라는 Origin에서 오는 Request만 접근을 허용하고 싶다면 Access-Control-Allow-Origin: https://my-site.com 과 같은 방식이다.	
	브라우저는 Origin과 Access-Control-Allow-Origin을 비교하여 유효한지 확인한다.

실제 CORS가 동작하는 방식은 아래 세 가지 시나리오에서 확인한다.
1. Preflight Request
일반적으로 웹 앱을 개발할 때 마주치는 시나리오. 브라우저는 Request를 한번에 보내지 않고 Preflight와 실제 Request로 나누어서 전송한다.\
Preflight Request에 OPTIONS 메소드가 사용된다. 실제 Request를 보내기 전 해당 Request를 보내는 것이 안전한지 확인한다.\
Preflight에는 Origin에 대한 정보 뿐만 아니라 Access-Control-Requeset-Headers나 Access-Control-Request-Method와 같은 실제 Request에서 사용할 요청에 대한 정보도 함께 포함되어 있다.\
이에 대한 Response의 Access-Control-Allow-Origin 필드의 값과 Request의 Origin이 다르다면 실제 Request는 CORS를 위반하여 CORS에러를 출력한다.
2. Simple Request
어떤 경우에는 Preflight를 보내지 않고 실제 Request를 전송하고, 이에 대한 Response의 Access-Control-Allow-Origin과 비교하여 CORS 위반을 확인하기도 한다.\
* 이 때 Request의 Method는 GET, HEAD, POST 중 하나여야 하며,\
* Accept, Accept-Language, Content-Language, Content-Type, DPR, Downlink, Save-Data, Viewport-Width, Width를 제외한 헤더를 사용하면 안된다.\
* 만약 Content-Type 헤더를 사용하는 경우에는 application/x-www-form-urlencoded, multipart/form-data, text/plain만 사용할 수 있다.\
위의 세 조건을 만족하는 경우에는 Preflight없이 실제 Request만 전송한 후 CORS 위반 여부를 판별한다.
3. Credentialed Request
브라우저가 제공하는 비동기 요청 API인 XMLHttpRequest나 fetch는 별도의 옵션 없이 브라우저의 쿠키 정보나 인증 관련 헤더를 Request에 추가하지 않는데, 이를 가능하게 해주는 옵션이 credentials 옵션이다.\
credentials에 같은 출처에서만 인증 정보를 담을 수 있는 기본값인 same-origin이나 모든 요청에 인증 정보를 담지않는 omit이 아닌, 항상 인증정보를 담는 include를 했을 경우, Access-Control-Allow-Origin과 함께 아래 두 가지 조건을 만족해야 한다.\
* Access-Control-Allow-Origin에는 와일드카드(\*)를 사용할 수 없다.
* Response Header는 반드시 Allow-Control-Allow-Credentials: true를 포함해야 한다.

## CORS 해결
가장 간단하게는 Response에서 Access-Control-Allow-Origin 헤더에 알맞은 값을 세팅해주는 것이다.\
와일드카드를 사용하면 모든 Request에 CORS를 해결하므로 편리하지만, 보안상으로 매우 안좋다.\
혹은 FE에서 프록시를 설정하여 데이터를 BE에서 직접 가져다가 유저에게 전달하는 방법도 있다.

검색 엔진에서는 CORS에 얽메이지 않는, SOP의 예외 조항을 통해서 Request를 처리하고 있다.\
\<img\>, \<script\> 스크립트, 이미지, 스타일시트 등과 같이 말이다.\
이러한 방식으로 Request를 처리하면 CORS를 위반하지 않고, Request를 성공한다.\
이 Request의 Header에는 sec-fetch-mode: no-cors라는 값이 포함되어 있으며, 이 필드를 통해서 CORS 검사를 skip하는 것이다.\
다만 브라우저는 이 Request의 응답을 JS에 보여주지 않기 때문에, 코드 레벨에서 이 응답에 담긴 내용에 접근 할 수 없다.\
Front에서 다루기 정말 힘들 것 같은데, 코드에서 해당 값에 접근을 못하게 한다는 점이 보안적으로는 굉장히 +인 것 같다.

---

# TTL
Time-to-live, Network Layer에서 0~255의 값을 가진 패킷의 유효 기간을 설정한다.\
한 라우터를 지날 때마다 값에서 1을 제하며, 0 이하의 값이 되면 더 이상 패킷이 유효하지 않다고 판단하여 패킷을 버리고, Host에게 이를 알린다.

---

# Keep-Alive
HTTP/1에서 사용하는 Request Header\
Connection을 재사용하기 위해서 비연결형인 HTTP/1 연결을 일정 시간동안 유지해달라는 의미\
연결은 유지하지만 HTTP/2처럼 멀티플렉싱이 되지 않으므로 보틀넥을 겪게 된다.

---

# Proxy VS Reverse Proxy
Request의 Identity를 숨기기는 서버 (= 그와 동시에 해당 프록시에 연결된 사람을 인증하는 도구가 될 수도 있음)\
Proxy가 Caching을 돕기도 한다.\
Traffic Control (Unwanted Sites Blocking) 가능\
GeoFencing (지리적으로 사이트 접근 차단 가능) \

Reverse Proxy를 사용하는 경우 Client는 어떤 서버에 접속하는지 알 수 없다.\
Load Balancer의 역할을 하는 것을 제외한다면 Proxy와 같다.\

---

# Stateful VS Stateless
Stateful은 클라이언트가 요청을 전송한 뒤, 서버가 응답을 하길 잠시 기다린다. 응답이 없다면 계속해서 요청을 전송한다.\
TCP, FTP 등\

Stateless는 클라이언트 요청의 State에 따라, 서버가 응답한다. 서버가 클라이언트에 대한 정보(세션)을 기억할 필요가 없다.\
UDP, HTTP/1, HTTP/2 등

---

# Network Scalability
Unix의 /proc/sys/fs/file-max는 OS에서 동시에 사용할 수 있는 fd의 갯수를 명시한다. *현재 사용중인 랩톱에서는 9223372036854775807라고 출력된다.*\
따라서 C10M의 문제가 되는 것은 Kernel의 문제가 아니다.\
실제로 문제가 되는 것은 CPU와 Memory이다. 프로그램 작성 시 1M+의 커넥션을 관리하기 위해서 수 GB의 메모리가 필요하다.\
또한 Outbound TCP Connection은 한 IP에서 PORT \~65000까지로 제한되어 있으므로 이 또한 서버의 Scalability에 걸림돌이된다. *OS Kernel의 문제가 아니라, TCP의 문제이다.*\
이 문제에 대해 자세히 설명된 [링크](http://highscalability.com/blog/2013/5/13/the-secret-to-10-million-concurrent-connections-the-kernel-i.html)

---

# Active/Active VS Active/Passive
High Availability를 위한 서버 세팅\
* Active/Passive
같은 VIP를 공유하는 두 Reverse Proxy(Load Balancer)를 이용하는 서버에 접근할 때, 한 RP가 ARP 요청을 수신하는 Active 역할, 다른 RP가 Passive 상태가 되는 것.\
만약 Master RP가 죽으면, 기존의 Worker RP가 Master(Active) 역할을 하게 된다.\
Bottle neck이 생기기 쉽지만, 설정하기 쉽다.

* Active/Active
N개의 VIP를 가진 DNS가 동일한 VIP를 공유하는 모든 RP(각각의 RP는 한 VIP의 마스터로, 한 VIP의 Backup으로 설정)에 1:1로 요청을 전달하는 것.\
모든 RP는 Active하게 요청을 수행한다.\
DNS에서 여러 VIP를 가진 Active/Active구조는 더 높은 Availability를 보인다.\
Request가 균등하게 분배되지만, 설정이 어렵고, 비용이 더 소모된다.

---

# Failover
클라이언트가 서버에 연결할 때, 서버가 죽으면 클라이언트가 즉시 다른 서버로 연결하는 것\
개발자는 IP 주소를 통해서 통신하지만, Lower Level에서는 실제로 MAC을 사용하여 통신한다.\
개발자가 사용하는 IP와 MAC 주소 변환을 돕는 것이 ARP (Address Resolution Protocol)이다.\
MAC이 진행되는 방식은 아래와 같다.

1. 사용자가 10.0.0.1이라는 가상의 주소에 요청을 보낸다.
2. 클라이언트는 10.0.0.1이라는 주소를 찾기위해 모든 네트워크에 10.0.0.1이 있는지를 체크한다.
3. 서버(10.0.0.1)은 자신의 MAC 주소를 알려준다.

VIP가 사용되는 시나리오는 아래와 같다.

1. 10.0.0.1(MAC Address: AAA)와 10.0.0.2(MAC Address: BBB)가 있을 때, 어떠한 에이전트 소프트웨어를 설치하여 Master와 Backup Node를 설정한다.
2. 두 노드는 가상의 IP인 VIP를 10.0.0.100으로 설정한다.
3. 클라이언트에서 10.0.0.100을 찾기위해 네트워크 상의 모든 호스트에 10.0.0.100에 대한 정보를 찾을 때, 실제 IP는 10.0.0.100이 아닌 두 노드 중 Master는 이 요청에 응답한다.

*마스터가 죽는다면, 꾸준히 헬스체크를 하던 백업 노드는 마스터가 응답이 없다는 것을 알게되고 10.0.0.100에 대한 요청에 대해 대신 응답한다. 하지만 헬스체크를 위한 시간이 소요되기 때문에 그 사이에 도착한 클라이언트의 요청은 제대로 응답되지 않을 수 있다.*

위와 같이 동작하는 Protocol을 VRRP(Virtual Router Redundency Protocol)이라고 한다.

---

# ARP
Layer Level 2 (Data Link Layer)에서 Frame을 어디로 전송할지 (Machine의 주소)를 알기위해서 MAC을 사용한다.\
대부분의 경우 (DNS를 통해 얻은) IP 주소를 알고 있지만, MAC을 아는 경우는 극히 드물다.\
ARP Table은 cached IP-MAC mapping으로, 이전에 ARP Request를 통해서 알게된 IP-MAC Mapping을 저장한다.

---

# Load Balancing in Layer 4 VS Layer 7
* Layer 4 Load-balancing
Transport Layer는 IP, PORT에 대한 정보를 다룬다\
따라서 Layer 4 Load Balancer는 Transport Layer에서 Request의 Source, Destination의 IP, PORT를 각각 Load Balancer와 Destination으로 바꿔서 전달한다.\

**클라이언트/로드밸런서 -> 로드밸런서/서버**

로드밸런스 방식이 간단하며, 데이터를 decrypt하지 않으므로 더 효율적이고 안전할 수 있다. 그리고 하나의 TCP Connection을 사용한다.\
하지만 데이터에 따른 Load Balancing이 불가능하다. 따라서 Micro Service Architecture에 적합하지 않다. 또한 만약 Request가 Segmentation되어 있다면 이를 설정해주는 로직이 필요하다. Caching이 불가능하다.

* Layer 7 Load-balancing
Application Layer에서 동작하므로, Request의 데이터를 읽을 수 있다.\
클라이언트로부터 Request를 수신하고 새로운 Request를 서버로 전송한다.\
서버로부터 응답을 받으면 그 응답을 클라이언트로 전달한다.\
(내가 만든 로드밸런서가 이 역할을 하는 Reverse-Proxy이다.)

데이터에 접근할 수 있으므로, smart load balancing이 가능하며, caching 역시 가능하다. 앞의 이유로 micro service에 적합하다.\
리소스 expensive하다. 데이터를 decrypt하기위해 certificate을 가지고 있어야한다.(TLS를 사용하는 경우) 새로운 TCP Connection을 생성한다.

---

# ALPN is critical for HTTP/2 Backends
HTTP2를 지원하지 않는 서버에 HTTP/2 Request를 보내면 fail!\
클라이언트는 HTTP/1로 다시 Request를 보내지만, 이미 시간/리소스의 낭비이다.\
그렇다면 "HTTP/2 Request를 요청하고, 만약 서버가 HTTP/2를 지원하지 않는다면 HTTP/1 Response를 요청한다."를 어떻게 효율적으로 나타낼 수 있는가?\
이 때 사용되는 것이 ALPN(Application Layer Protocol Negotiation)이다.\
TCP Handshake 후, TLS Handshake가 진행될 때(CA로부터 공개키를 건네 받고, 대칭키를 만들어서 서버에게 돌려줄 때) HTTP/2로 통신을 원하고, 만약에 지원하지 않는다면 HTTP/1로 통신을 할 것임을 알린다.\ 

---

# Chromium supports HTTP/3!
크롬이 HTTP/3 지원을 시작했다.\
크롬 내부적으로 어떤 방식으로 작동하는지는 아직 모르겠으나, ALPN을 DNS에 적용하고있다고 한다.\
그래서 google.com에 접속하겠다고하면, DNS가 google은 udp를 쓴다고 알려주고 브라우저는 자연스럽게 tcp가 아닌 udp를 사용하는 것이다.\
google은 이미 상당 부분을 HTTP/3로 포팅한 상태이다.

---

# QUIC
* Built-in Security
TLS를 대체할 QUIC의 Transport Layer에서의 보안은 기존의 three-way handshake를 포함한다. 하지만 TCP/TLS1.3과는 다르게 1번의 round-trip으로 완성된다.\

	// TCP + TLS HTTP Request
	CLIENT		TCP SYN->			SERVER
	CLIENT		<-TCP SYN + ACK		SERVER
	CLIENT		TCP ACK->			SERVER
	CLIENT		TCP ClientHello->	SERVER
	CLIENT		<-TCP ServerHello	SERVER
	CLIENT		TCP Finished->		SERVER
	CLIENT		HTTP Request->		SERVER
	CLIENT		<-HTTP Response		SERVER
	
	// QUIC HTTP Request
	CLIENT		QUIC->				SERVER
	CLIENT		<-QUIC				SERVER
	CLIENT		QUIC->				SERVER
	CLIENT		HTTP Request->		SERVER
	CLIENT		<-HTTP Response		SERVER

* HTTP/2와 마찬가지로 Stream을 추가 (Tranport Layer에서 처리)

* Head-of-line Blocking
HTTP/2에 있던 Transport Layer의 head-of-line blocking 제거

* Connection 개념을 접목

* Reliability

* NAT Gateway에서의 단점
NAT Router는 아직 QUIC 프로토콜과 호환되지 않는 경우가 많음

*Method, headers, body 등 HTTP의 req, res 구성은 동일하게 가져가지만, binary data over multiplexed QUIC이라는 점에서 HTTP1(ASCII over TCP), HTTP2(binary multiplexed over TCP)와 차이를 보인다.*

따라서 HTTP3는 아래의 모델로 구성된다.

	HTTP/3
	QUIC(+TLS 1.3)	// Stream을 담당, HTTP/2는 Application Layer에서 Stream을 담당
	UDP
	IP

단점은 3-7%의 QUIC 통신은 실패하는 것으로 보이며, 이에 대한 fallback이 필요함\
Linux에서 UDP의 optimization이 되어있지 않아서 2~3배의 CPU 사용량을 보인다.

---

# Cookie
## Creating Cookies
1. JS - Document.cookie를 통해서 mapping
2. Web Server - Set-cookie header를 통해서 browser가 server 대신 cookie를 설정

## Cookie Properties
1. Sent with every request
2. Cookie Scope

	// Domain
	document.cookie = "test=test; domain=.test.com;";
	// 위 코드는 .test.com과 패턴 매칭되는 모든 도메인에 test=test 쿠키를 설정한다.
	
	// Path
	document.cookie = "test=test; path=/testpath";
	// 위 코드는 코드의 path와 접근하는 웹페이지의 path가 같을 때에 쿠키를 설정한다.

3. Expires, Max-age
Browser Process가 종료되면 사라지는 Session Cookie VS Browser를 종료하고 다시 실행해도 유지되는 Permanent Cookie를 구분하는 cookie\
expires는 cookie가 만료될 날짜를, max-age는 만료될 때까지의 시간을 millisecond로 환산해서 입력받는다.\
Explorer를 제외한 브라우져들은 두 cookie를 혼용 가능하며, explorer는 expires만 인식한다.\
일반적으로 max-age를 사용한다.

4. Same site
과거에는 cookie에 session이 저장된 상태에서 3rd party에서 링크를 통해서 다른 도메인에 request를 보내는 형태의 해킹을 할 수 있었다. -> CORS를 통해서 block!\
하지만 cookie에서도 samesite=strict를 통해서 같은 사이트에 접속할 때만 쿠키를 설정하도록 할 수 있다.

## Cookie Types
* (Session Cookie)[#cookie-properties]
* (Permanent Cookie)[#cookie-properties]
* Httponly Cookie - httponly; 를 포함하여 document.cookie로부터 접근할 수 없는 쿠키, browser가 document.cookie에게 해당 쿠키를 보여주지 않고 보관하다가 server에 제공.
* Secure Cookie - secure flag를 사용하여 HTTPS scheme에게만 해당 쿠키 제공
* Third Party Cookie - 다른 도메인에서 설정하는 쿠키, SOP object의 src에서 쿠키를 설정할 수도 있다. 이 경우에는 다른 도메인으로 쿠키를 건네주는 tracking이 가능하다. 실제로 ads, statistics에서 주로 사용한다.
* Zombie Cookie - 쿠키를 삭제하더라도 스스로 재생성하는 쿠키. 일반적으로 쿠키를 삭제하고 같은 도메인에 재접속할 때, 기존의 세션은 없어져야하지만, 쿠키가 아닌 다른 정보(connection, indexed db, etag 등)을 통해서 사용자를 인식하고 다시 같은 쿠키를 제공할 경우, 이를 Zombie cookie라고 한다.

*e-tags: 클라이언트가 서버에 request를 보냈을 때, 서버는 etag를 생성하여 client에 전달한다. 쿠키와 동일한 기능을 수행하지만 쿠키와 다른 형태로 저장된다.*

## Cookie Security
* Stealing Cookie - document.cookie를 읽고 이 쿠키를 다른 서버에 전송
* Cross Site Request Forgery - A 도메인에서 B.com/transfer?account=someone%amount=999999 와 같은 방식으로 사용자의 쿠키를 사용

---

# alt-svc VS ALPN
내 답변
Depending on what you want, 'alt-svc' header might do. 
At first, I thought you meant a TCP client (web-browser) trying to connect to a UDP server. Which doesn't work. But I just realised there is another scenario, in which a TCP client (web-browser) connects to a TCP server, then the server responds with some 'alt-svc' headers, such as 'alt-svc: h3-Q050=":443"; ma=2592000'. This header triggers the client's web-browser to try to connect to the host using the given protocol and port.


I'm not sure whether this can be considered ALPN, since this alt-svc header is included in the application-data(response), not in one of those TLS handshake messages. Anyway, it does the job. If you want to know more about it, check out RFC7301, RFC7639.

---

# E-Tags
Overhead를 막기위해 고안된 header 중 하나\
Client가 Server에 어떠한 데이터를 요청하면, Server는 요청된 데이터와 함께 E-tag을 전송한다.\
Client가 다시 같은 데이터를 요청하며 전달받은 E-tag을 If-None-Match 헤더와 함께 전송한다.\
만약 데이터가 변하지 않았을 경우 Server는 304 Not Modified Response를 Return한다. Built-in Cache라고 생각할 수 있다.

*하지만 최근에는 잘 사용하지 않는다.*
Load Balancer를 통해서 다수의 Server가 연결되어 있다고 가정할 때, 한 Server는 다른 Server와 서로 다른 Etag을 생성할 수 있다.\
이 때 etag은 오히려 더 많은 Overhead를 만들게 된다.\
*위의 문제는 Apache, NginX 등의 서버에서 자체적으로 솔루션을 제공한다.*

또한 Etag을 사용해서 tracking을 하는 경우가 많다.\
Etag는 Cookie와 다르게 브라우저가 직접 관리하므로 사용자가 접근할 수 없기 때문에, tracking에에 사용된다.\
예를 들어 image src의 서버가 계속 Not Modified 응답을 하는 경우, 해당 image의 etag은 항상 같게 유지되어 image src의 서버가 사용자를 track 할 수 있다.\
위의 문제들로 인해 Etag은 점점 더 사라져가고 있으며, Browser 역시 etag을 삭제하는 방법을 지원하는 등 etag을 지양하는 방향으로 발전하고 있다.

---

# Session Layer
*Provide a session between two hosts*
*Internally to the computer if there is a bottleneck there is a backlog and something needs to manage what needs to be sent, what no longer needs to be sent and what priority the data to be sent has this something is a session.*
Session은 SYN과 FIN 사이에 존재한다.\
Presentation Layer와 함께 Transport Layer에 기능을 더하는 용도로 사용된다.

Session Layer는 다음과 같은 서비스를 제공한다.
* Dialogue Management - 여러 Process가 동시에 통신을 할 때(Network Interface 자원 요청), 어떤 Process가 통신을 할 것인지 순서를 정한다.
* Synchronisation - Transport Layer는 통신 상의 에러만 catch한다. 하지만 Synchronisation은 그보다 상위 레벨의 에러를 다룬다. 예를 들어 FTP 통신에서 Transport Layer는 옳게 데이터를 전송했지만, Application Layer는 File System의 문제로 데이터를 전달받지 못할 수도 있다.
* Activity Management - 
* Exception Handling
*.. TCP/IP Protocols do not include a session layer at all. ... By Worcester Polytechnic Institute*

일반적으로 RPC에 사용된다고 한다.(RPC에 SESSION LAYER가?)\
여기서 문제는 일반적으로 웹 프로그래밍을 할 때 일컫어지는 RPC는 TCP/IP Protocol을 따르며 REST와 같은 HTTP를 사용하되 Endpoint와 Payload의 차이가 있을 뿐이다.\
검색 결과 RPC는 어떠한 프로토콜에 한정된 것이 아닌 패러다임이라고 하기 때문에, "Session Layer를 사용하는 RPC Implementation이 있다."고 생각하는 편이 낫지 않을까?

---

# TLS
통신을 할 때 내 Node의 Router는 내 Private IP를 Public IP로 전환한다.\
일반적으로 모든 Packet은 ISP로 바로 전달되지만, Internet은 기본적으로 다른 Node를 통해서 전달되는 데이터의 흐름이므로 100% 안전하다고 할 수 없다.\
따라서 TLS의 Goal은 Connection을 중개하는 다른 Node가 중간에서 connection(source/destination ip, port)을 제외한 데이터를 sniff(Deep-Packet Inspection) 하지 못하도록 암호화하는 것이다.\
Certificate은 client가 접근하는 server가 실제 server가 맞는지를 확인시켜준다.\
Client도 certificate을 가지고 server가 이를 확인하는 형태를 Mutual TLS라 한다. 이는 한 application이 여러 서비스로 나눠진 Micro Service Architecture에서 중요하다.(대부분의 MicroService는 Mutual TLS등 complexity를 피하기 위해서 K8S와 같은 cluster에 deploy한다.)\

---

# AWS ALB, NLB and CLB
* NLB
Network Connection(IP addr, port)에 따라서 Layer4(transport layer)에서 load balancing한다.\
content-type, cookie 등 application layer의 criteria는 사용되지 않는다.\
NAT Gateway의 logic을 통해서 구현되었으며, EIP를 사용하기 때문에 static한 endpoint를 가지게 된다.

* ALB
Layer3(Network Layer)부터 Layer7(Application Layer)까지의 정보를 종합하여 load balancing한다.\
HTTP(1.1, 2)와 HTTPS를 rule-based, host-based, path-based로 load balancing 가능하다.

Neetwork LoadBalancer는 단순히 request를 forwarding하는 반면 Application LoadBalancer는 Request를 확인하고 Content-Based-Route한다.\
또한 NLB의 경우 application의 availability를 확신할 수 없다. Server의 Ping에 대한 응답이나 3-Way TCP Handshake 가능 여부를 통해서 availability를 따지기 때문이다.\
반면 ALB의 경우 HTTP GET Request에 대한 응답이나, response의 content가 예상한 대로 나오는지 등 더 자세히 확인할 수 있다.

* CLB
Classical LoadBalancer는 Legacy이며 Backward-compatibility 등 특별한 경우가 아니라면 사용을 권장하지 않는다.

---

# Netmask
Netmask는 "Subnet에 얼마나 많은 IP가 있을 수 있는지를 나누는(available hosts)" 32bit으로 구성된 mask이다.\
255.255.255.0은 항상 Network address로 지정되어 있으며, 255.255.255.255는 항상 Broadcast address로 지정되어있어서 할당할 수 없다.\
아래 예시와 같이 subnet을 나타낸다.

    IP                  NETMASK             DESC
    192.168.55.161      255.255.255.255     192.168.55.161
    192.168.55.0        255.255.255.0       192.168.55.0    - 192.168.55.255
    192.168.55.240      255.255.255.240     192.168.55.240  - 192.168.55.255
    192.168.55.161      255.255.255.0       192.168.55.0    - 192.168.55.161
    192.168.0.0         255.255.0.0         192.168.0.0     - 192.168.255.255

---

# Auth & JWT
1. Storing PW as is
최악, DB Leak의 경우 PW 노출

2. Storing Hashed PW
PW를 알 수 없지만, DB Leak의 경우 PW 예측 가능

3. Storing Salt and Hashed PW
Salt로 Hash된 PW와 Salt를 저장, 2 Column을 추가해야하는 Overhead 발생

4. Storing Hashed PW that stores Salt
bcrypt 등을 사용하여 hashed pw가 salt를 포함하도록 한다.

5. Always ask the PW and store something else
매번 PW를 묻고 PW와 기타 데이터를 조합한 무언가를 저장한다.

* Using JWT
위의 모든 방법은 application은 stateless하더라도 db가 stateful하다. System 전체로 봤을 때, stateful하다고 볼 수 있다.\
Stateless, Non-Session based의 방법으로 JWT를 사용하며, login token, reload token을 사용한다.

---

# DNS over HTTPS
Request가 발생하면 PORT 53 (UDP)를 통해서 DNS Provider(주로 ISP)에 해당 Domain의 IP를 요청&전달하게 된다.\
HTTPS 보안을 통해서 Payload가 보이지 않는다고 하더라도, 해당 Request가 향하는 Domain은 보이기 때문에 이를 통해서 정부&기관은 Block이 가능하다.\
FireFox는 이것을 막기위해서 CloudFlare에 Secure Connection을 연결한 후 DNS를 Query하는 DNS over HTTPS를 고안했지만 TCP Handshake 중에도 Domain이 노출되어 근본적인 해결책이 아니라는 취약점이 있다.

--- 

# Virtual IP Address (VIP)
Master Node는 Virtual IP에 응답한다.\
Health Check를 통해서 Slave(Worker) Node는 Virtual IP에 응답하지 않는다.\
Master가 Unresponsive되면 Slave Node는 Master가 되어서 Virtual IP에 응답한다.\
위의 과정을 VRRP (Virtual Router Redundancy Protocol)이라고 한다.\
LoadBalancer가 있으니 필요없다고 생각할 수도 있지만, entry point를 늘린다는 점에서 만약에 entry point load balancer가 여러개 있다면? 더더욱 Highly Available하지 않은가?를 알 수 있다.

---

# NAT Slipstreaming
Packet을 특정한 방식으로 만들면 NAT Gateway는 이를 해독하는 과정(Deep Packet Inspection)에서 PORT OPEN과 같은 Malicious 명령을 수행할 수도 있다.

---

# google.com and www.google.com are different
Browser는 HTTPS로 연결되는 도메인을 저장하고 이후에 해당 도메인에 접근하는 Request가 발생하면 바로 HTTPS 연결을 시도한다.(HSTS)\
하지만 www를 붙이지 않으면, browser는 저장된 도메인과 일치하지 않다고 인식하고 HTTP 연결을 시도한다.\
뿐만 아니라 대부분의 사이트는 HTTP 연결 시에 HTTPS로 redirect를 반환하므로 1번의 Round Trip이 낭비된다.\
결과적으로 보안 측면에서, 그리고 속도 측면에서도 google.com이 아닌 www.google.com을 추천한다.

---
