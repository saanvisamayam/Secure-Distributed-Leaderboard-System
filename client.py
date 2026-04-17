import socket
import ssl

# 🔴 CHANGE THIS to your server IP
HOST = "192.168.1.45"   # example → replace with YOUR IP
PORT = 5050

# Create SSL context
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap with TLS
secure_client = context.wrap_socket(client_socket, server_hostname=HOST)

# Connect to server
secure_client.connect((HOST, PORT))

print("Connected to Secure Leaderboard Server")

while True:

    print("\n1 Update Score")
    print("2 Get Leaderboard")
    print("3 Ping Server")
    print("4 Exit")

    choice = input("Choice: ")

    if choice == "1":

        name = input("Player Name: ")
        score = input("Score: ")

        msg = f"UPDATE {name} {score}"

        secure_client.send(msg.encode())

        response = secure_client.recv(1024).decode()

        print(response)

    elif choice == "2":

        secure_client.send(b"GET")

        data = secure_client.recv(4096).decode()

        print("\nLeaderboard\n")
        print(data)

    elif choice == "3":

        secure_client.send(b"PING")

        response = secure_client.recv(1024).decode()

        print("Server:", response)

    elif choice == "4":

        print("Closing connection...")
        break

    else:
        print("Invalid option")

secure_client.close()