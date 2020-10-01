# Introduction
## Layering
네트워크 프로토콜은 일반적으로 각각의 역할을 가진 레이어로 이루어져있다. TCP/IP 모델은 4단계로 이루어져있다. (OSI와 TCP/IP는 같은 것을 두 가지로 나타낸 것이 아니라, OSI는 일반적인 통신에 대한 개념을, TCP/IP는 TCP/IP모델에 한정된 프로토콜의 집합을 나타낸 것이다.)\
 네트워크가 소규모 컴퓨터들의 집합을 나타내던 1980년대 초와는 다르게 그러한 근거리 네트워크의 집합이 된 1990년대에는 기존의 간단한 모델에서 벗어나 더 많은 기능성이 추가된 Transport Layer와 Network Layer를 분리해야된다는 것을 알게된다.\
여러 네트워크를 연결하는 가장 쉬운 방법은 Gateway라고도 불리는 Router를 통해서이다. Router는 네트워크를 연결하기 위한 특수한 하드웨어로, Network Interface Layer의 이더넷, 토큰링 등 다양한 물리적 네트워크와 호환이 된다.(다수의 Network Layer들을 하나의 LAN으로 연결하는 Bridge라는 방법도 있지만, 이는 잘 사용되지 않는다.)\
이렇듯 여러 레이어로 구성되어 한 레이어는 다른 레이어와 별개로 작동하는 것이 인터넷의 가장 큰 장점이다. 우리는 Kernel이 구성하는 Transport Layer, Network Layer, 하드웨어 레벨의 Network Interface Layer를 직접 설정하지 않고 Application Layer만 구성함으로써 인터넷을 사용할 수 있는 것이다.

---

## TCP/IP Layering
TCP는 reliable(패킷의 전달을 신뢰할 수 있음)하지만 TCP의 바탕이 되는 IP는 reliable하지 않다. (UDP 는 reliable하지 않다.)\
IP는 Network Layer의 중심이 되는 프로토콜이다. 클라이언트와 서버, 각 엔드 뿐만 아니라 Router 역시 Network Link Layer와 Network Layer까지 다룬다.

---

## Internet Address
인터넷 상의 모든 인터페이스는 Unique한 인터넷 주소(IP 주소)를 가져야 한다.\
기존에 사용되는 IPV4는 32bit으로 이루어져있으며 0~255까지의 4개의 정수를 .으로 구분하여 나타낸다.\
IPV4가 나타내는 2^32-1개의 IP 주소는 인터넷의 폭발적인 성장과 함께 빠르게 동날 것이라고 예상되었기 때문에, 128비트의 수를 8그룹의 16진수의 4가지 숫자로 나타내어지는((2^4) * 4 * 8) IPV6도 혼용하기 시작한다.\
인터넷의 모든 인터페이스에 unique한 인터넷 주소를 배정하기 위해서 InterNIC가 네트워크의 ID를 부여하며, HOST ID를 제공하는 것은 sysAD에게 달려있다.\
IPV4의 경우 주소를 구성하는 4개의 정수 중 가장 앞의 정수에 따라 Class (쓰임)이 나뉘게 되며, IP 주소 자체도 unicast(single host), broadcast(네트워크의 모든 호스트), multicast(네트워크의 멀티캐스트 그룹), 3가지 타입으로 나뉘게 된다.

---

## Encapsulation
Ethernet의 프레임은 46~1518바이트로 구성된다.\
IP(Network Layer)와 Network Interface(Network Interface Layer) 사이에 전달되는 것은 Packet으로 IP Datagram (혹은 일부)를 뜻한다.

---

## Client-Server Model
대부분의 네트워크 Application은 클라이언트-서버 모델로 정의할 수 있다.\
이는 서버가 클라이언트에게 어떠한 서비스를 제공하는 모델을 뜻한다.\
서버는 다시 iterative/concurrent로 정의할 수 있다\
* Iterative
	1. 클라이언트 요청을 기다린다.
	2. 요청을 수행한다.
	3. 응답한다.
	4. 1로 돌아가 요청을 기다린다.

* Concurrent
	1. 클라이언트 요청을 기다린다.
	2. 요청을 수행할 새로운 서버를 시작하고 1로 돌아간다. (Multi-process/Multi-thread)
	3. 요청을 수행한 서버는 종료된다.

*책이 옛날 책이라서 Concurrent에 Async는 나와있지 않다. 새로운 서버를 시작하는 것은 아니지만 Concurrent에 Async 모델을 추가해야 될 것이다.*

일반적으로 TCP는 Concurrent, UDP는 Iterative를 적용한다.

*왜 UDP에는 Iterative를 적용하는게 일반적이지? 옛날 기준인가? 하나하나의 DG에 대해서 Concurrent한 흐름을 만들면 DG를 관리하기 어려워서인가? 스트리밍 서비스가 Iterative한 Logic을 사용해서 Request를 처리하면 퍼포먼스가 안 나올것 같은데?*

---

## APIs
TCP/IP Application에 주로 사용되는 API는 Socket과 TLI가 있다.

*Socket = 네트워크 통신의 추상화라는 일반적인 설명X, Berkeley에서 개발한 TCP/IP 통신을 위한 API*

---
---

# Link Layer
