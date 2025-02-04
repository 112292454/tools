PORT = 16017
UPLOAD_DIR = "./"

import http.server
import socketserver
import os
import cgi


class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            print('rcv upload request')
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            upload_path = form.getvalue('path', '/')
            file_name = form['file'].filename
            file_path = os.path.join(UPLOAD_DIR, upload_path, file_name)
            print(file_path)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as f:
                f.write(form['file'].file.read())

            self.send_response(200)
            self.end_headers()
            # self.wfile.write(b'文件上传成功，请重启SD ui\n')
            self.wfile.write(f'文件上传成功，请重启SD ui\n'.encode('GBK'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'post Not found\n')

    def do_GET(self):
        if self.path == '/':
            self.send_response(302)  # 302 表示临时重定向
            self.send_header('Location', '/up/upload.html')  # 重定向到 /upload_success
            self.end_headers()
            # 你可以在这里处理上传页面的返回
            pass
        else:
            super().do_GET()  # 让 SimpleHTTPRequestHandler 处理文件服务

Handler = CustomRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("Server running at port", PORT)
httpd.serve_forever()