# 局域网实时语音通话 | LAN Real-time Voice Call

> 打开浏览器即可加入的局域网多人语音通话：浏览器之间走 WebRTC 点对点直连，服务器只负责撮合信令。仅供可信局域网使用。
> Multi-party voice calls on your LAN straight from the browser: audio streams peer-to-peer via WebRTC while the server only exchanges signaling. For trusted LANs only.

## 功能特性 | Features

- **WebRTC 点对点**：音频不经过服务器中转，延迟低、音质好；进入页面自动与所有在线设备建连（ID 较小者主动发起 offer）。
  **Peer-to-peer WebRTC**: audio never relays through the server; connections to all online peers are established automatically on page load (the device with the smaller ID initiates the offer).
- **纯标准库后端**：`server.py` 仅用 Python 标准库（ThreadingTCPServer + ssl），以 2 秒心跳轮询完成信令交换（`/api/heartbeat`、`/api/push`、`/api/online`）。
  **Standard-library-only backend**: `server.py` (ThreadingTCPServer + ssl) exchanges signaling via 2-second polling (`/api/heartbeat`, `/api/push`, `/api/online`).
- **强制 HTTPS**：WebRTC（getUserMedia）要求安全上下文，服务器以自签证书包裹。
  **HTTPS enforced**: WebRTC (getUserMedia) requires a secure context, so the server wraps itself with a self-signed certificate.

## 快速开始 | Quick Start

```bash
# 1) 首次使用先装依赖、生成证书（证书已被 .gitignore，克隆后必须跑一次）
# 1) Install deps and generate the certificate first (it is gitignored; run once after cloning)
pip install -r requirements.txt
python generate_cert.py

# 2) 启动服务器 | Start the server
python server.py
```

局域网设备访问 `https://<服务器IP>:5000`，首次访问需在浏览器中信任自签证书。
Other LAN devices open `https://<server-IP>:5000` and trust the self-signed certificate on first visit.

## 配置 | Configuration

| 项 | Item | 说明 | Notes |
|---|---|---|---|
| 端口 | Port | 硬编码 `5000`（`server.py`） | Hard-coded `5000` in `server.py` |
| 证书 | Certificate | `generate_cert.py` 生成 10 年期自签证书（SAN 含本机局域网 IP） | `generate_cert.py` creates a 10-year self-signed cert (SAN includes the LAN IP) |

## 说明 | Notes

- ⚠️ **证书不会自动生成**：缺少 `server.crt` / `server.key` 时服务器会直接启动失败，务必先跑 `generate_cert.py`。
  ⚠️ **Certificates are NOT auto-generated**: the server fails to start without `server.crt` / `server.key` — run `generate_cert.py` first.
- 生成脚本依赖 `cryptography` 库；服务器运行本身零第三方依赖。
  The generator needs `cryptography`; the running server itself has zero third-party dependencies.
- 心跳 5 秒超时即从在线列表移除；仅限可信局域网使用。
  Devices drop off the online list after a 5-second heartbeat timeout. Trusted LANs only.
