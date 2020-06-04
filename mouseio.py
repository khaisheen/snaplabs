from pynput.mouse import Listener, Button, Controller
import socketio, eventlet, numpy as np

HOST = 'localhost'
PORT = 3000
ADDR = (HOST,PORT)
mouse = Controller()

def on_click(x, y, button, pressed):
    if button == Button.right:
        return False
    print("CLICK!!!, pressed=",pressed)

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
    
@sio.on('my data', namespace='/')
def mydata_handler(sid, msg):
    print('Message received:', msg)
    while CONNECTED:
        event = 'my data'
        data = [mouse.position[0], mouse.position[1]]
        sio.emit(event, data)
        print('Emitted:', event, data, '\n')
        sio.sleep(1/30)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(ADDR),app)    
    try:
        listener = Listener(on_click=on_click)
        listener.start()
        while listener.running:
#            print(f"x={mouse.position[0]}, y={mouse.position[1]}")
            sio.sleep(1/30)
    except KeyboardInterrupt:
        listener.stop()
            
            
            
            
            
            
            
            
            
