#  Secure Distributed Leaderboard System

##  Project Overview

This project implements a **secure, multi-client leaderboard system** using **low-level TCP socket programming** in Python.

Multiple clients can connect to a central server to:

* update player scores
* retrieve a ranked leaderboard
* communicate securely over a network using **SSL/TLS encryption**

The system demonstrates key concepts of:

* Network programming
* Concurrency
* Secure communication
* Protocol design
* Performance evaluation

---

##  Objectives

* Implement **TCP-based client-server communication**
* Enable **secure communication using SSL/TLS**
* Support **multiple concurrent clients**
* Design a simple **application-layer protocol**
* Evaluate system **performance under load**

---

##  System Architecture

The system follows a **multi-client client–server architecture**:

```id="arch123"
           TLS + TCP
Client 1 -----------\
Client 2 ------------> Server (Leaderboard)
Client 3 -----------/
```

###  Server Responsibilities

* Maintains leaderboard data
* Handles multiple client connections
* Processes commands
* Tracks performance metrics
* Ensures secure communication

###  Client Responsibilities

* Connects to server
* Sends commands
* Displays responses

---

## Communication Protocol

The system uses a simple **text-based protocol**:

| Command               | Description           |
| --------------------- | --------------------- |
| UPDATE <name> <score> | Update player score   |
| GET                   | Retrieve leaderboard  |
| PING                  | Check server response |

### Example

```id="proto123"
UPDATE Alice 120
GET
```

---

##  Security (SSL/TLS)

* All communication is encrypted using **TLS**
* A **self-signed certificate (`cert.pem`) and private key (`key.pem`)** are used
* Prevents packet sniffing and data tampering

---

##  Technologies Used

* Python
* socket programming
* threading
* SSL/TLS (`ssl` module)
* JSON (persistent storage)

---

##  Setup Instructions

###  Clone / Download Project

```id="setup1"
secure-leaderboard/
```

---

###  Generate Certificates

```id="setup2"
python generate_cert.py
```

Generates:

```id="setup3"
cert.pem
key.pem
```

---

###  Run Server

```id="setup4"
python server.py
```

---

###  Run Client

```id="setup5"
python client.py
```

---

##  Multi-Device Deployment

* Server runs on one machine
* Clients connect using server IP address

Example:

```id="deploy1"
Server IP: 192.168.1.45
PORT: 5050
```

Client configuration:

```id="deploy2"
HOST = "192.168.1.45"
PORT = 5050
```

---

##  Features Implemented

*  TCP socket communication
*  SSL/TLS encryption
*  Multi-client support (threading)
*  Leaderboard ranking system
*  Persistent storage (JSON file)
*  Input validation & error handling
*  Rate limiting (anti-spam)
*  Performance monitoring

---

##  Performance Metrics

The system evaluates performance using:

1. Active Clients
2. Peak Clients
3. Total Requests
4. Throughput (requests/sec)
5. Latency (per request)
6. Average Latency
7. Error Rate
8. Requests per Client
9. Min/Max Latency

---

##  Performance Evaluation

### Sample Output

```id="perf123"
Active Clients: 10
Peak Clients: 12
Total Requests: 50
Throughput: 5.2 req/sec
Latency: 0.002 sec
Average Latency: 0.003 sec
Error Rate: 0/50
```

---

##  Load Testing

A separate script simulates multiple clients.

Run:

```id="load123"
python load_test.py
```

* Simulates 10+ concurrent clients
* Generates multiple requests
* Helps evaluate system scalability

---

##  Performance Analysis

* Throughput increases with number of clients
* Latency slightly increases under high load due to thread scheduling
* TLS introduces minor overhead but ensures secure communication
* System handles concurrent requests efficiently

---

##  Optimizations

* Thread-based concurrency for parallel client handling
* Lock mechanism to prevent race conditions
* Input validation to prevent invalid data
* Rate limiting to prevent excessive requests

---

##  Edge Cases Handled

* Invalid commands
* Incorrect UPDATE format
* Non-integer scores
* Empty leaderboard
* Client disconnection
* SSL handshake failures

---

##  Conclusion

This project demonstrates a **secure and scalable networked system** using:

* TCP socket programming
* TLS encryption
* Multi-threaded concurrency
* Performance monitoring

It reflects real-world distributed system design principles.

---

##  Team Contributions

* **Member 1**: Problem definition, architecture, protocol design
* **Member 2**: Socket programming, concurrency implementation
* **Member 3**: Security (TLS), performance analysis, optimization

---

##  Future Improvements

* Database integration (MySQL / MongoDB)
* GUI-based client interface
* Deployment on cloud server
* User authentication system

---
