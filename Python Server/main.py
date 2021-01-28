from http.server import BaseHTTPRequestHandler, HTTPServer
from configfileIO import updateEvents, readConfigs, updateTicker, updateVideo, updateTime, getTime
from pathlib import Path
import threading
import time

'''
To install bluetooth lib:
git clone https://github.com/pybluez/pybluez.git
cd pybluez
python setup.py install
'''

is_on = True
bt_ok = True
try:
    import bluetooth as bt
except:
    print('No bluetooth module')
    bt_ok = False

try:
    if bt_ok:
        bt_sock = bt.BluetoothSocket(bt.RFCOMM)
        bt_port = 5
        mac_addr = '98:3B:8F:EB:F2:E3'
        bt_sock.connect((mac_addr, bt_port))
except:
    print('Bluetooth port on server side not open')
    bt_ok = False

host = ''
PORT = 21000

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
        self.send_header("Access-Control-Allow-Headers",
                         "X-Requested-With, Content-type")

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
            pass
            # self.update_video(post_body, ctype)

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
        global is_on
        bodyType = body_dict['type']

# Update events
        if bodyType == 'event':
            updateEvents(body_dict)
# Update banner
        elif bodyType == 'banner':
            print("updating banner...")
            bannerpath = contentpath / "banner.png"
            print(bannerpath)
            data = bytes(eval(body_dict['data']))
            with open(bannerpath, "wb") as f:
                f.write(data)
            print("done updating banner!")

# Update ticker
        elif bodyType == 'ticker':
            updateTicker(body_dict)
# Update video
        elif bodyType == 'video':
            updateVideo(body_dict)
            
# Update time
        elif bodyType == 'time':
            updateTime(body_dict)
            
# Manual on/off
        elif bodyType == 'manual':
            cmd = body_dict['data']
            print(cmd)
            if bt_ok and cmd == '"on"' and not is_on:
                print('ON')
                bt_sock.send('on')
                is_on = True
            elif bt_ok and cmd =='"off"' and is_on:
                print('OFF')
                bt_sock.send('off')
                is_on = False   


#HTTPServer((host, PORT), HandleRequests).serve_forever()

def server_thread_func():
    print("Running Python Server...")
    HTTPServer((host, PORT), HandleRequests).serve_forever()

def auto_on_off_thread_func():
    global is_on

    if not bt_ok:
        return
    current_time = time.strftime("%H%M", time.localtime())
    counter = 0
    while counter < 2:
        next_time = time.strftime("%H%M", time.localtime())
        if current_time != next_time:
            current_time = next_time
            # print(current_time)
            on_time, off_time = getTime()
            if current_time == on_time and not is_on:
                bt_sock.send('on')
                is_on = True
            elif current_time == off_time and is_on:
                bt_sock.send('off')
                is_on = False
            #bt_sock.send('off' if is_on else 'on')
            #is_on = not is_on 
            # counter += 1
        time.sleep(5)
    bt_sock.send('q')
    bt_sock.close()


server_thread = threading.Thread(target=server_thread_func, args=())
server_thread.start()

bt_thread = threading.Thread(target=auto_on_off_thread_func, args=())
bt_thread.start()



        
