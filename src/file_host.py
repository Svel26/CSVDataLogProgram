from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json
import sys

class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file_host.py <config_path>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    config = load_config(config_path)

    input_directory_path = config['input_directory']
    output_directory_path = config['output_directory']
    server_host = config.get('server_host', 'localhost')
    server_port = config.get('server_port', 8000)
    
    os.chdir(output_directory_path)

    server_address = (server_host, server_port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Serving at http://{server_host}:{server_port} from directory {output_directory_path}")
    httpd.serve_forever()