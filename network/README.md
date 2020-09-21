# HTTP/1.1
Application 레이어에서 정의된 프로토콜\
연결 상태를 유지하지 않음(비연결성)\
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
* Layered System - API Response 뿐만 아니라 Authentication 등의 계층 추가 용이
RPC의 경우 Resource의 이름/구분이 아닌 Function에 대해 Request를 보내는 차이가 있을 뿐, 어느 패러다임이 더 우수/열등하다고 할 수 없다.

---

# gRPC
Protocol Buffer라는 Message라는 미리 설정된 (Static) Bytes 형식으로 Payload를 encoding하여 역시 미리 설정된 Service라는 RPC Function을 향해 HTTP/2 환경에서 통신하는 RPC 형태의 프레임워크\
통신 순서
* Client가 Stub Method (Parameter와 Return 타입, Service명)를 Call하면 Server는 Client의 Metadata를 전송받고, 바로 Metadata를 전송할지 Request Body를 전송받고 Metadata를 전송할지 결정한다.
* Client의 Request를 전송받고 로직을 실행한 뒤 서버는 Trailing Metadata와 함께 Response를 전달한다.
* gRPC Call이 발생하면 gRPC Client는 Server와의 Connection을 생성한다. 6~8개의 connection을 생성할 수 있는 HTTP와는 다르게 HTTP/2에서 한 개만 생성할 수 있는 Connection은 무제한한 갯수의 bi-directional stream을 생성할 수 있다.

---

# HTTP/2
TCP/IP Layer 중 Application Layer에 Binary Framing Layer가 추가되어 아래의 기능이 HTTP/1.1보다 향상되었다.
* Header 압축을 통해서 latency 줄임
* 한 개의 커넥션에서 Concurrent한 데이터 교환 가능
* 기본 단위는 Frame으로 Header와 Data Frame은 HTTP/1.1의 Request, Response에 해당하며, 이를 제외한 Settings 등의 Frame은 HTTP/2의 Feature를 담당한다.
* Connection은 양방향으로 Stream을 가지고 있기 때문에, Blocked, Stalled로 인해서 Progress에 영향을 끼칠 염려가 적다.
* Flow Control은 각 Stream이 서로에게 영향을 끼치지 않도록 제어하는 역할을 한다. 예를 들어 의존성이 있는 스트림의 순서 정렬, 중요도에 의한 리소스 배정과 같은 것이다.
* Prioritisation은 Headers Frame의 priority attribute에 따라 Resource 점유에 우선순위를 두는 것이다.
* Multiplexing: Multiple different server requests are allowed simultaneously, on the same connection. With HTTP/1.1, each additional requests for assets would have to wait until the previous transfer in the queue completed. This decreases complexity in development, not necessitating things like asset bundling to decrease to number of server requests. 한 스트림 내에서 다수의 Request를 Frame으로 분할하여 다수의 Request/Response를 동시에 처리

---

#JWT(Json Web Token)
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
* Network는 네트워크 상에서 패킷의 이동, 어떤 경로를 통해 패킷을 전달할 것인가를 다룬다. 공유기 - 라우터 - 이더넷 - 파이버 - 이더넷 - 서버와 같은 특정 경로를 Session(세션)이라고 부른다.
* Network Interface는 네트워크에 접속하는 하드웨어 계층을 담당한다.

IP(Network Layer)는 패킷의 배송을 담당한다. 목적지의 위치 (IP와 MAC 주소)를 참조하여 그 다음 라우터로 데이터를 전송한다.\
TCP(Transport Layer)는 신뢰성을 담당한다. 데이터를 TCP Segment라고 불리는 Packet으로 조각내고, 도착했는지를 3-Way Handshake을 통해서 확인한다.

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

OSI의 레이어
* Application - 사용자가 Interact하는 Layer
* Presentation - OS가 Application Layer의 데이터를 받아서 변환, 암호화 등을 담당하는 Layer
* Session - Connection의 일부인 Session을 구축하는 Layer
* Transport - 데이터를 Packet으로 자르고, 어떤 크기의 Packet으로 데이터 통신을 할 것인지 담당하는 Layer
* Network - 노드 사이의 논리적인 경로를 결정하는 Layer
* Network Link - 하드웨어 + 소프트웨어적으로 데이터 운송을 담당하는 Layer
* Physical - 하드웨어 레벨에서 데이터 운송을 담당하는 Layer

---

# HTTPS
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
* TCP는 가상 회선 방식을 제공하여 논리적인 경로(Session)을 배정한다. 연결형 서비스이며, Packet이 전달되었는지를 확인하고, 전달이 되지 않았다면 다시 전달 하는 등 신뢰성을 보장하지만, 연결 설정, 해제에 자원이 필요하여 UDP에 비해 속도가 느리다.
* UDP는 논리적인 경로를 설정하지 않기 때문에, 전달하는 각각의 Packet은 다른 경로로 전달된다. 비연결형 서비승기 때문에 연결을 설정, 해제하는 과정이 없다. 신뢰성보다 속도가 더 중요한 Streaming 서비스에 주로 사용된다.

---

# Socket 통신
Socket 통신은 Request에 대한 Response 응답 후 연결을 끊는 HTTP 통신과 달리 Server와 Client가 특정 Port를 통해 연결을 유지하여 실시간으로 양방향 통신이 가능한 통신 방식이다.\
HTTP는 Client만 Request를 보내고 Server는 이에 응답하는데 반해 Socket 통신은 Server가 Client에게로 먼저 데이터를 보낼 수 있으며, 연결을 해제하기 전까지 계속 연결을 유지하는 연결지향형 통신이기 때문에 실시간 통신이 필요한 게임, 채팅 등에 주로 사용된다.

---

# Forward VS Redirect
* Forward는 URI에 전달된 Request를 서버가 Target URI에 전달한다. 전달받은 URI에서 버는 클라이언트에게 Response를 리턴한다.
* Redirect는 서버가 클라이언트에게 새로운 URI로 Request를 보내라는 신호를 전달한다. 클라이언트는 새로운 URI에 새로운 Request를 보낸다.
*새로고침 등을 했을 때, 같은 데이터를 보내는 문제를 피하기 위해서 Redirect를 사용한다. 하지만 조회 등의 간단한 기능에는 Forward를 사용해도 된다*.

---

# A Record & CNAME
A 레코드는 DNS와 IPV4를 연결하는 방식이다. 이에 반해 CNAME은 DNS에 대한 또 다른 DNS라고 볼 수 있다. 
	someURI.abc -> properURI.com
CNAME을 사용하여 DNS나 IP가 바뀔 때마다 이에 맞춰 다른 사양 역시 변갱해야되는 일을 피할 수 있다.

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
Stateful Protocol(TCP)를 사용할 때, Connection은 (Source IP, Source Port, Destination IP, Destination Port) 형태의 튜플로 구성된다. 따라서 서로 다른 클라이언트가 동일한 서버에 접속한다고 Connection이 충돌하는 경우는 없다.\
만약 같은 클라이언트 or 서로 다른 클라이언트가 NAT이나 공유기를 통해서 한 서버에 접속한다해도, 서버가 인식하는 Source Port는 NAT Gateway나 공유기의 서로 다른  Port가 되므로 Connection은 구분이 가능하다.\
만약에 Connection의 Source IP, Source PORT가 같다면 이 Connection들은 같은 Connection으로 인식된다.

---

# HTTP/2 - More
대부분의 브라우저는 여러 Request를 보내야 할 때, 여러 Connection을 만들어서 각 Request 사이의 Latency를 줄인다. 하지만 Connection이 많아지면 Server의 Overhead가 커진다는 단점이 있다. 그렇기 때문에 HTTP/2가 생겼다.
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

# Session VS Session
세션에는 두 가지 의미가 있다.\
우리가 웹 애플리케이션에서 상태 유지를 위해서 사용하는 것도 세션이고, TCP/IP 모델에서 Network Layer가 결정하는 Logical한 경로도 Session이다.\
앞의 세션은 로그인 혹은 상태 유지 시에 클라이언트의 쿠키에 의미 없는 데이터를 주고, 이를 서버 사이드의 데이터베이스와 비교하는 방식으로 작동한다.\
뒤의 세션은 Network Layer에서 패킷을 보낼 경로를 결정하고 Connection이 유지되는 동안 이 경로를 유지한다. (연결을 유지할 것인가는 Transport Layer가 결정하지만, 경로를 설정하는 것은 Network Layer가 담당한다.)\
뒤의 세션의 경우 OS Level에서 작동하므로 보통 개발자가 다루는 경우는 드물다.\

---

# Load Balancing Techniques
* Round Robin - 연결되어 있는 노드에 순서대로 돌아가면서 트래픽을 전달하는 방식
* Weighted Round Robin - 각각의 노드에 Weight를 주어 우선 순위를 배정하는 것
* Least Connection - 현재 가장 적은 수의 커넥션이 연결되어 있는 노드에 트래픽 전달
* Weighted Least Connection - Least Connection 방식에 Weight 적용
* Resource Based - 노드에 서비스를 설치하여 현재 사용 중인 리소스에 따라서 트래픽을 배정한다.

---

#HTTPS SECURITY - 2
인터넷 사이트는 CA에 공개키를 제공한다.\
CA는 CA의 개인키로 인터넷 사이트의 정보를 암호화하여 인증서를 발급한 후, 자신의 공개키를 웹브라우저에 제공한다.\
사용자가 인터넷 사이트에 접속하면 인증서를 웹 브라우저에 보내고, 사용자는 CA의 공개키로 인증서를 복호화하여 사이트의 정보와 공개키를 받는다.\
공개키로 대칭키를 암호화하여 사이트에 보낸다.\
사이트는 개인키로 데이터를 복호화하여 대칭키를 생성하고, 이제 대칭키를 통해서 통신한다.\
세션이 종료되면 대칭키를 폐기한다.\
*대칭키는 매번 사용할 때마다 다른 키가 생성되므로 비교적 안전하고, 공개키보다 속도가 빠르다는 장점도 있다.*

HTTPS를 사용할 경우 암호화, 복호화에 시간이 소요되므로 속도가 느려지게 되며, CA의 인증서를 생성하고 유지하는데 비용이 필요하다.\
암호화된 데이터를 캐싱할 수 없기 때문에 이를 위한 별도의 스텝이 필요하다.\
특정 프레임워크에서 지원하지 않는다면 기존에 존재하는 URI를 HTTPS 프로토콜로 변경해야한다.

---














