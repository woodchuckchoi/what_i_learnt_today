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
