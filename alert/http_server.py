from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socketserver
import socket
import threading
import time

class ServerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.path.endswith("/alert"):
                content_length = int(self.headers['Content-Length'])
                post_body = self.rfile.read(content_length).decode()
                data = json.loads(post_body)
                alert_info = data['alerts'][0]
                print(alert_info)
        except IOError:
            self.send_error(404, "Not Found")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 19092
    Handler = ServerHandler
    httpd = ThreadedHTTPServer((HOST, PORT), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    time.sleep(60)
    httpd.shutdown()
    httpd.server_close()