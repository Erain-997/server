import socket
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def run_server(host, port):
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print("Running at {}:{} ...".format(host, port))
    httpd.serve_forever()


class MyRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if self.path == '/friend':
            response = self.friend_handler(data)
        elif self.path == '/create_account':
            response = self.create_account_handler(data)
        else:
            response = {"status": "error", "message": "Unknown API"}

        self._set_response(200)
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def friend_handler(self, data):
        # 处理好友逻辑
        # 示例：返回成功的响应
        return {"status": "success", "message": "Friend added"}

    def create_account_handler(self, data):
        # 处理帐号创建逻辑
        # 示例：返回成功的响应
        return {"status": "success", "message": "Account created"}
