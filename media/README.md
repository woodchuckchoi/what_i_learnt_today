# Everything you need to know about streaming protocols

```
Online video delivery uses both streaming protocols and HTTP-based protocols. Streaming protocols like Real-Time Messaging Protocol (RTMP) enable speedy video delivery using dedicated streaming servers, whereas HTTP-based protocols rely on regular web servers to optimize the viewing experience and quickly scale. Finally, a handful of emerging HTTP-based technologies like the Common Media Application Format (CMAF) and Apple’s Low-Latency HLS seek to deliver the best of both options to support low-latency streaming at scale.
```

```
Selecting the right protocol starts with defining what you’re trying to achieve. Latency, playback compatibility, and viewing experience can all be impacted. What’s more, content distributors don’t always stick with the same protocol from capture to playback. Many broadcasters use RTMP to get from the encoder to server and then transcode the stream into an adaptive HTTP-based format.
```

## Most Common Protocols Used for Streaming

* Traditional Streaming Protocols
	* RTMP (Real-Time Messaging Protocol)
	* RTSP (Real-Time Streaming Protocol)/RTP (Real-Time Transport Protocol)

* HTTP-Based Adaptive Protocols
	* Apple HLS (HTTP Live Streaming)
	* Low-Latency HLS
	* MPEG-DASH (Moving Picture Expert Group Dynamic Adaptive Streaming over HTTP)
	* Low-Latency CMAF for DASH (Common Media Application Format for DASH)
	* Microsoft Smooth Streaming
	* Adobe HDS (HTTP Dynamic Streaming)

* New Technologies
	* SRT (Secure Reliable Transport)
	* WebRTC (Web Real-Time Communications)

### Traditional Streaming Protocols

```
Traditional streaming protocols, such as RTSP and RTMP, support low-latency streaming. But they aren’t supported on all endpoints (e.g., iOS devices). These work best for streaming to a small audience from a dedicated media server.

RTMP delivers video at roughly the same pace as a cable broadcast — in just over five seconds. RTSP/RTP is even quicker at around two seconds. These protocols achieve this by transmitting the data using a firehose approach rather than requiring local download or caching. But because very few players support these protocols, they aren’t optimized for great viewing experiences at scale. Many broadcasters choose to transport live streams to the media server using a stateful protocol like RTMP and then transcode it into an HTTP-based technology for multi-device delivery.
```

* RTMP
	* Audio Codecs: AAC, AAC-LC, HE-AAC+ v1 & v2, MP3, Speex
	* Video Codecs: H.264, VP8, VP6, Sorenson Spark®, Screen Video v1 & v2
	* Compatibility: Limited to Flash Player, Adobe AIR, RTMP-compatible players. No longer accepted by most devices.
	* Specification: TCP

* RTSP/RTP
	While RTSP is a presentation-layer protocol that lets end users command media servers via pause and play capabilities, RTP is a transport protocol used to move said data.
	* Audio Codecs: AAC, AAC-LC, HE-AAC+ v1 & v2, MP3, Speex, Opus, Vorbis
	* Video Codecs: H.265 (preview), H.264, VP9, VP8
	* Compatibility: Not widely supported

---

### Adaptive HTTP-Based Streaming Protocols

```
Streams deployed over HTTP are not technically “streams.” Rather, they’re progressive downloads sent via regular web servers. Using adaptive bitrate streaming, HTTP-based protocols deliver the best video quality and viewer experience possible — no matter the connection, software, or device. Some of the most common HTTP-based protocols include MPEG-DASH and Apple’s HLS.
```

* Apple HLS
	Apple HLS supports adaptive bitrate streaming, which is key to viewer experience. Content distributors encoded streams into many different bitrates and broke them into fragments. These multi-bitrate chunks would then be indexed in a manifest file and delivered to the player.
	* Audio Codecs: AAC-LC, HE-AAC+ v1 & v2, xHE-AAC, Apple Lossless, FLAC
	* Video Codecs: H.265, H.264
	* Compatibility: Great

* MPEG-DASH
	* Audio Codecs: Codec-agnostic
	* Video Codecs: Codec-agnostic
	* Compatibility: Good

---

### New Technologies

```
WebRTC, and SRT were designed with latency in mind.
```

* SRT
	* Audio Codecs: Codec-agnostic
	* Video Codecs: Codec-agnostic
	* Compatibility: Limited

* WebRTC
	WebRTC is a combination of standards, protocols, and JavaScript APIs that enables real-time communications (RTC, hence its name). Users connecting via Chrome, Firefox, or Safari can communicate directly through their browsers — enabling sub-500 millisecond latency.
	* Audio Codecs: Opus, iSAC, iLBC
	* Video Codecs: H.264, VP8, VP9
	* Compatibility: Chrome, Firefox, Safari

---

# WebRTC

WebRTC는 크게 media capture devices와 peer-to-peer connectivity로 이루어진다.

* Media Capture Devices
```
Media capture devices includes video cameras and microphones, but also screen capturing "devices". For cameras and microphones, we use navigator.mediaDevices.getUserMedia() to capture MediaStreams. For screen recording, we use navigator.mediaDevices.getDisplayMedia() instead.
```

* Peer-to-Peer Connectivity
```
The peer-to-peer connectivity is handled by the RTCPeerConnection interface. This is the central point for establishing and controlling the connection between two peers in WebRTC.
```

WebRTC Protocol은 아래와 같이 이루어지지만, WebRTC의 requirements에 맞추기 위해서는 WebSocket, XHR 등의 프로토콜 역시 필요하다.
```
RTCPeerConnection, DataChannel
SRTP, SCTP
Session (DTLS: Datagram Transport Layer Security)
ICE, STUN, TURN
Transport(UDP)
Network(IP)
```
ICE, STUN, TURN은 UDP 상에서 peer-to-peer connection을 체결하고, 유지하기 위해서 사용되며, DTLS는 WebRTC에 필수적인 encryption을 UDP 상에서 구현하기 위해서 사용되는 Protocol이다.\
SCTP와 SRTP는 Application Layer Protocol로 여러 스트림 사이에서 multiplexing을 구현하기 위해서 사용된다.

HOW ICE WORKS

```
First, it tries to connect peers directly via UDP.
If UDP fails, it tries TCP.
If both UDP and TCP direct connection fail, which is often the case in real scenarios because of NATs and firewalls, ICE will first use a STUN server with UDP to connect peers. A STUN server is a server that implements the STUN protocol and is used to find the public address and port of a peer behind an asymmetric NAT.
If the STUN server fails, ICE will use a TURN server, which is a STUN server with some extra relaying functionalities that can traverse symmetric NATs.
```

```
Media streams are encrypted using Secure Real-time Transport Protocol (SRTP) and data streams are encrypted using Datagram Transport Layer Security (DTLS).
Access to camera and microphone has to be granted by the client. To keep the client aware, browsers show icons if the device’s camera or microphone is active.
All WebRTC components run in the browser sandbox and use encryption, they don’t need any kind of installation, they will just work as long as the browser supports them.
```

