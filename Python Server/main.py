from http.server import BaseHTTPRequestHandler, HTTPServer
from configfileIO import updateEvents, readConfigs, updateTicker
from pathlib import Path

host = ''
PORT = 99

contentpath = Path(__file__).parent.parent / "Content/Files"

configsfile = contentpath / "configs.txt"

class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
#        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
#        self.send_header("Content-type", "text/xml")
        self.end_headers()    
        
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        
    def do_GET(self):
        self._set_headers()
        data = readConfigs()
#        print(events)
        self.wfile.write(data.encode('utf-8'))
        
    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        ctype = self.headers.get('content-type')
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        if("multipart/form-data" in ctype):
            self.update_video(post_body, ctype)
        
        else:
            bodystring = post_body.decode("utf-8")
    #        print(bodystring)
    #        print(type(bodystring))
            body_dict = eval(bodystring)
            
            
            self.update_configs(body_dict)
            
    #        print(eval(bodystring))
    #        self.send_header("Content-length", str(len(body)))
    #        self.wfile.write(b"received: " + (post_body))
            self.wfile.write(b"DONE THANKS")
        
    def update_configs(self, body_dict):
        widgetType = body_dict['type']
        
# Update events
        if widgetType == 'event':
            updateEvents(body_dict)
# Update banner
        elif widgetType == 'banner':
            print("updating banner...")
            data = bytes(eval(body_dict['data']))
            with open(contentpath / "banner.png", "wb") as f:
                f.write(data)
            print("done updating banner!")   
            
# Update ticker
        elif widgetType == 'ticker':
            updateTicker(body_dict)
# Update video            
        elif widgetType == 'video':
            pass
            
            
#    def update_video(self, body, ctype):
#        print("updating video...")
#        parts = decoder.MultipartDecoder(body, ctype).parts
#        print(parts)
#        for part in parts:
#            print(part.headers)  
#            print(part.encoding)
#            print(part.text)
#        print("done updating video!")
#            

HTTPServer((host,PORT),HandleRequests).serve_forever()