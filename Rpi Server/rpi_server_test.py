import bluetooth 
import time
import requests

off_hour = 22
on_hour = 8
DEVICE_IP = '192.168.4.18'
url1 = 'http://'
url2 = ':6095/controller?action=keyevent&keycode='

def press(key):
    url = url1+DEVICE_IP+url2+key
    print(url)
    requests.post(url)
    return True

def on():
    attempts = 0
    while attempts < 3:
        try:
            press('power')
            attempts = 3
        except:
            print('unable to access URL')
            attempts +=1

def off():
    try:
        press('power')
        time.sleep(0.5)
        press('right')
        time.sleep(0.5)
        press('right')
        time.sleep(0.5)
        press('enter')
    except:
        print('unable to access URL')
        return False




server_sock  = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 5
server_sock.bind(("", port))
server_sock.listen(1)

while True:
    print("Waiting for connection")
    client_sock, address = server_sock.accept()
    print("Accepted connection from ", address)

    counter = 0
    while True:
        data = client_sock.recv(1024).decode('utf-8')
        print (f"received: {data}")
        
        if data == '':
            counter += 1

        if data == 'on':
            #on()
            counter = 0
            print('ON')
        
        elif data == 'off':
            #off()
            counter = 0
            print('OFF')
        
        elif data == 'q' or counter > 30:
            break

    client_sock.close()

server_sock.close()