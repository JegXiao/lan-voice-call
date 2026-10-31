import http.server, socketserver, json, socket, ssl, os
from voice_logic import manager


class VoiceHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # 屏蔽串口所有访问报告

    def do_GET(self):
        if self.path == '/':
            self.serve_file('chat.html')
        elif self.path == '/api/online':
            self.send_json(manager.get_online_list())
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        client_ip = self.client_address[0]

        if self.path == '/api/heartbeat':
            manager.update_device(client_ip, data['id'])
            self.send_json(manager.pull_signals(data['id']))
        elif self.path == '/api/push':
            manager.push_signal(data)
            self.send_json({"status": "ok"})

    def serve_file(self, file):
        with open(file, 'rb') as f:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f.read())

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


if __name__ == '__main__':
    PORT = 5000
    # 获取局域网IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    LOCAL_IP = s.getsockname()[0]
    s.close()

    print("=" * 60)
    print(f"🚀 语音通信中心已就绪")
    print(f"🌐 本地访问: https://localhost:{PORT} 或 https://127.0.0.1:{PORT}")
    print(f"📱 局域网访问: https://{LOCAL_IP}:{PORT}")
    print("=" * 60)

    httpd = socketserver.ThreadingTCPServer(('0.0.0.0', PORT), VoiceHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()