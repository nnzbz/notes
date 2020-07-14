# WebRTC笔记-01.入门

[TOC]

## 1. WebRTC 简介

WebRTC （Web Real-Time Communications）是一项实时通讯技术，它允许网络应用或者站点，在不借助中间媒介的情况下，建立浏览器之间点对点（Peer-to-Peer）的连接，实现视频流和（或）音频流或者其他任意数据的传输。

## 2. WebRTC支持的平台

| [Chrome](http://chrome.google.com/) | [Firefox](https://www.mozilla.org/en-US/firefox/new/) | [Opera](http://www.opera.com/) | [Safari](https://webrtc.org/native-code/ios/) | [Android](https://webrtc.org/native-code/android/) | [iOS](https://webrtc.org/native-code/ios/) |
| :---------------------------------: | :---------------------------------------------------: | :----------------------------: | :-------------------------------------------: | :------------------------------------------------: | :----------------------------------------: |
|    ![chrome](chrome-128x128.png)    |            ![firefox](firefox-128x128.png)            |  ![Opera](opera-128x128.png)   |         ![apple](Safari-128x128.png)          |          ![android](android-128x128.png)           |        ![apple](apple-128x128.png)         |
|              Latest ✔               |                       Latest ✔                        |            Latest ✔            |                     11+ ✔                     |                      Latest ✔                      |                   11+ ✔                    |

## 3. WebRTC的三个模块

- Voice Engine（音频引擎）  
  - Voice Engine包含iSAC/iLBC Codec（音频编解码器，前者是针对宽带和超宽带，后者是针对窄带）  
  - NetEQ for voice（处理网络抖动和语音包丢失）  
  - Echo Canceler（回声消除器）/ Noise Reduction（噪声抑制）  
- Video Engine（视频引擎）  
  - VP8 Codec（视频图像编解码器）  
  - Video jitter buffer（视频抖动缓冲器，处理视频抖动和视频信息包丢失）  
  - Image enhancements（图像质量增强）  
- Transport (传输)
  - SRTP（安全的实时传输协议，用以音视频流传输）  
  - Multiplexing（多路复用）  
  - P2P，STUN+TURN+ICE（用于NAT网络和防火墙穿越的）  
  - 除此之外，安全传输可能还会用到DTLS（数据报安全传输），用于加密传输和密钥协商
  - 整个WebRTC通信是基于UDP的

## 4. WebRTC 的核心组件  

- 音视频引擎：OPUS、VP8 / VP9、H264  
- 传输层协议：底层传输协议为 UDP  
- 媒体协议：SRTP / SRTCP  
- 数据协议：DTLS / SCTP  
- P2P 内网穿透：STUN / TURN / ICE / Trickle ICE  
- 信令与 SDP 协商：HTTP / WebSocket / SIP、 Offer Answer 模型

## 5. WebRTC 音频和视频引擎  

![WebRTC音频和视频引擎](WebRTC音频和视频引擎.png)  

- 最底层是硬件设备，上面是音频捕获模块和视频捕获模块  
- 中间部分为音视频引擎。音频引擎负责音频采集和传输，具有降噪、回声消除等功能。视频引擎负责网络抖动优化，互联网传输编解码优化  
- 在音视频引擎之上是 一套 C++ API，在 C++ 的 API 之上是提供给浏览器的Javascript API

## 6. WebRTC 协议栈  

![WebRTC协议栈](WebRTC协议栈.png)

- WebRTC 核心的协议都是在右侧基于 UDP 基础上搭建起来的  
- 其中，ICE、STUN、TURN 用于内网穿透, 解决了获取与绑定外网映射地址，以及 keep alive 机制  
- DTLS 用于对传输内容进行加密，可以看做是 UDP 版的 TLS。由于 WebRTC 对安全比较重视，这一层是必须的。所有WebRTC组件都必须加密，并且其JavaScript API只能用于安全源（HTTPS或本地主机）。信令机制并不是由WebRTC标准定义的，所以您必须确保使用安全协议。  
- SRTP 与 SRTCP 是对媒体数据的封装与传输控制协议  
- SCTP 是流控制传输协议，提供类似 TCP 的特性，SCTP 可以基于 UDP 上构建，在 WebRTC 里是在 DTLS 协议之上  
- RTCPeerConnection 用来建立和维护端到端连接，并提供高效的音视频流传输  
- RTCDataChannel 用来支持端到端的任意二进制数据传输  
- WebRTC 协议栈解释  
  - ICE（Interactive Connectivity Establishment）
    互动式连接建立（RFC 5245）  
  - STUN(Session Traversal Utilities for NAT)
    只能UDP，告诉我暴露在广域网的地址IP port ，我通过映射的广域网地址进行P2P数据通信（RFC 5389）  
  - TURN(Traversal Using Relays around for NAT)
    UDP或TCP， 打洞失败后，提供服务器中转数据，通话双方数据都通过服务器，占服务器带宽较大 - 为了确保通话在绝大多数环境下可以正常工作（RFC 5766）  
  - SDP：会话描述协议（RFC 4566）  
  - DTLS：数据报传输层安全性（RFC 6347）  
  - SCTP：流控制传输协议（RFC 4960）  
  - SRTP：安全实时传输协议（RFC 3711）

## 7. JavaScript API  

- [getUserMedia()](https://webrtc.github.io/samples/src/content/getusermedia/gum/)：捕捉音频和视频  
- [RTCPeerConnection](https://webrtc.github.io/samples/src/content/peerconnection/pc1/)：在用户之间流式传输音频和视频  
- [RTCDataChannel](https://webrtc.github.io/samples/src/content/datachannel/basic/)：在用户之间传输数据  
- [MediaRecorder](https://webrtc.github.io/samples/src/content/getusermedia/record/)：录制音频和视频  
