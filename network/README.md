# HTTP/1.1
Application 레이어에서 정의된 프로토콜\
연결 상태를 유지하지 않음(비연결성)\
HTTP/1.1의 구성\
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
Resource의 이름이나 구분을 통해서 Resource에 대한 정보를 주고 받는 개발 패러다임
URI에 HTTP Method로 구분되는 Request를 보내고 그에 해당되는 Response 수신
특징
	* Stateless - 상태에 구애받지 않고 들어오는 요청만 수행한다.
	* Cacheable - GET과 같은 Method에 한해서 expires 헤더를 설정하면 브라우저는 caching
	* Layered System - API Response 뿐만 아니라 Authentication 등의 계층 추가 용이
RPC의 경우 Resource의 이름/구분이 아닌 Function에 대해 Request를 보내는 차이가 있을 뿐, 어느 패러다임이 더 우수/열등하다고 할 수 없다.

---

# gRPC
Protocol Buffer라는 Message라는 미리 설정된 (Static) Bytes 형식으로 Payload를 encoding하여 역시 미리 설정된 Service라는 RPC Function을 향해 HTTP/2 환경에서 통신하는 RPC 형태의 프레임워크
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
JSON Object를 Hash를 통해서 안전하게 전달하는 기술
Header, Payload, Signature로 구성된 JSON Object를 Base64형태로 치환하여 전달
	* Header에는 alg, typ(jwt)
	* Payload에는 데이터
	* Signature는 Header와 Payload를 Base64 encoding 후 private key(salt)를 이용하여 alg로 암호화
수신자는 public key를 사용하여 전달자의 정체를 알 수 있다.

---


