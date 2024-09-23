from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    os.chdir('.')
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Serving at http://localhost:8000")
    httpd.serve_forever()
