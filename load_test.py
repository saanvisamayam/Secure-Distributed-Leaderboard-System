import socket
import ssl
import threading

HOST = "YOUR_IP_HERE"
PORT = 5050

def simulate_client(id):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = context.wrap_socket(s, server_hostname=HOST)

    s.connect((HOST, PORT))

    for i in range(5):
        msg = f"UPDATE user{id} {i*10}"
        s.send(msg.encode())
        s.recv(1024)

    s.close()

threads = []

for i in range(10):   # 10 clients
    t = threading.Thread(target=simulate_client, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Load test completed")