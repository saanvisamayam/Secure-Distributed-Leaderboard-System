import socket
import threading
import ssl
import time
import json

HOST = "0.0.0.0"
PORT = 5050

leaderboard = {}
lock = threading.Lock()

request_count = 0
active_clients = 0
peak_clients = 0
total_latency = 0
error_count = 0
start_time = time.time()

metrics_lock = threading.Lock()


def save_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)


def load_leaderboard():
    global leaderboard
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
    except:
        leaderboard = {}


def update_score(player, score):
    with lock:
        if player in leaderboard:
            leaderboard[player] = max(score, leaderboard[player])
        else:
            leaderboard[player] = score
        save_leaderboard()


def get_leaderboard():
    with lock:
        sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        if not sorted_board:
            return "Leaderboard Empty"
        return "\n".join([f"{p} : {s}" for p, s in sorted_board])


def print_performance():
    elapsed = time.time() - start_time
    throughput = request_count / elapsed if elapsed > 0 else 0
    avg_latency = total_latency / request_count if request_count > 0 else 0

    print("\n---- PERFORMANCE ----")
    print(f"Active Clients: {active_clients}")
    print(f"Peak Clients: {peak_clients}")
    print(f"Total Requests: {request_count}")
    print(f"Throughput: {throughput:.2f} req/sec")
    print(f"Average Latency: {avg_latency:.4f} sec")
    print(f"Errors: {error_count}")
    print("---------------------\n")


def handle_client(conn, addr):
    global request_count, active_clients, peak_clients, total_latency, error_count

    with metrics_lock:
        active_clients += 1
        peak_clients = max(peak_clients, active_clients)

    print("Client connected:", addr)

    while True:
        try:
            request_start = time.time()

            data = conn.recv(1024).decode()
            if not data:
                break

            parts = data.split()

            if parts[0] == "UPDATE":
                if len(parts) != 3:
                    conn.send(b"Invalid format")
                    continue

                player = parts[1]
                try:
                    score = int(parts[2])
                except:
                    conn.send(b"Score must be integer")
                    continue

                update_score(player, score)
                conn.send(b"Score updated")

            elif parts[0] == "GET":
                board = get_leaderboard()
                conn.send(board.encode())

            elif parts[0] == "PING":
                conn.send(b"PONG")

            else:
                conn.send(b"Unknown command")

            request_end = time.time()
            latency = request_end - request_start

            with metrics_lock:
                request_count += 1
                total_latency += latency

            print_performance()

        except Exception as e:
            error_count += 1
            print("Error:", e)
            break

    conn.close()

    with metrics_lock:
        active_clients -= 1

    print("Client disconnected:", addr)


load_leaderboard()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(10)

print("Secure Leaderboard Server Running...")

while True:
    client_socket, addr = server.accept()

    try:
        secure_conn = context.wrap_socket(client_socket, server_side=True)

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()

    except ssl.SSLError:
        print("SSL Handshake Failed")