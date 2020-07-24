'''
Created on Apr 1, 2019

@author: Tavis
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from root.nested.data_handler import process_data

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Posted")
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len)
        print(data)
        print("Data Read Finished")
    
        #process data
        dict_data = json.loads(data)
        print(dict_data)
        result_text = process_data(dict_data)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result_text.encode("utf-8"))
        print("Sent")
        
    def do_GET(self):
        self.send_response(200)
        if self.path == '/':
            self.send_header("Content-type", "text/html")
            self.end_headers()
        
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == '/request.js':
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            
            with open("request.js", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("".encode("utf-8"))
server_address = ('', 8000)
httpd = HTTPServer(server_address, Handler)
httpd.serve_forever()