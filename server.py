import socket
import json
HOST = "localhost"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("server http://localhost:8080")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(8192).decode()
            if not data:
                continue

            head, body = data.split("\r\n\r\n", 1)
            lines = head.split("\r\n")
            method, path, version = lines[0].split(" ")

            headers = {}
            for line in lines[1:]:
                if ": " in line:
                    name, value = line.split(": ", 1)
                    headers[name] = value

            print(method, path)
            print(headers)
            print(body)

            if method == "GET" and path == "/":
                answer = open("index.html").read()
            elif method == "GET" and path.startswith("/page?id="):
                id = path.split("=")[1]
                answer = "page id = " + id
            elif method == "POST":
                try:
                    info = json.loads(body)
                    answer = "got json :: " +str(info)
                except:
                    answer = "bad json"
            else:
                answer = "not found"
            conn.sendall(("HTTP/1.1 200 OK\r\n\r\n" + answer).encode())




# run
#  python server.py
#  open http://localhost:8080 in browser

# test
#  curl http://localhost:8080/
#  curl "http://localhost:8080/page?id=67"
#  curl -X POST http://localhost:8080/api -H "Content-Type: application/json" -d "{\"name\": \"Vlad\"}"