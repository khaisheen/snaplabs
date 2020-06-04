from pynput.mouse import Listener, Button, Controller
import socketio, eventlet, numpy as np

# Server stuff
HOST = 'localhost'
PORT = 3000
ADDR = (HOST,PORT)

mouse = Controller()
clicked = False

# =============================================================================
# Listener for clicks
# =============================================================================

def on_click(x, y, button, pressed):
    global clicked
    print("CLICK!!!")
    clicked = pressed

# =============================================================================
# SocketIO server
# =============================================================================
    
sio = socketio.Server()
app = socketio.WSGIApp(sio)

CONNECTED = False

@sio.event
def connect(sid, environ):
    global CONNECTED
    CONNECTED = True
    print('connect ', sid)
    
@sio.event
def disconnect(sid):
    global CONNECTED
    CONNECTED = False
    print('disconnect ', sid)
    
# Emit stuff here
@sio.on('my data', namespace='/')
def mydata_handler(sid, msg):
    global clicked
    print('Message received:', msg)
    while CONNECTED:
        event = 'my data'
        data = {'x':mouse.position[0],
                'y':mouse.position[1],
                'pressed':clicked}
        sio.emit(event, data)
        print('Emitted:', event, data, '\n')
        sio.sleep(1/30)

# To turn off the server u gotta close the console, ctrl+C dont work
if __name__ == '__main__':
    try:
        listener = Listener(on_click=on_click)
        listener.start()    
        eventlet.wsgi.server(eventlet.listen(ADDR),app)    
#        while listener.running:
#            print(f"Listener:{clicked}")
#            print(f"x={mouse.position[0]}, y={mouse.position[1]}")
#            sio.sleep(1/30)
    except KeyboardInterrupt:
        listener.stop()
            
            
            
            
            
            
            
            
            
