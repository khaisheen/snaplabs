import socketio, eventlet, numpy as np

HOST = 'localhost'
PORT = 3000
ADDR = (HOST,PORT)

# =============================================================================
# Functions
# =============================================================================

def random_coords(minimum, maximum):
    coords = []
    num_ppl = np.random.randint(0,10)
    for j in range(18 * num_ppl):
        c = []      
        c.append(np.random.randint(minimum,maximum))
        c.append(np.random.randint(minimum,maximum))
        c.append(np.random.randint(minimum,maximum))
        coords.append(c)
    return coords

# =============================================================================
# The socket.io App
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
        data = random_coords(-1000,1000)
        sio.emit(event, data)
        print('Emitted:', event, data, '\n')
        sio.sleep(1/30)
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(ADDR),app)