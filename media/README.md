# Everything you need to know about streaming protocols

* RTMP, HLS, RTCP, RTP, etc

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


---

# WebRTC


