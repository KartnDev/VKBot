import datetime
import socketserver, socket

html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>The HTML5 Herald</title>
</head>
<body>
  Time
</body>
</html>
"""


def create_header(response_code: str, content_type: str = "text/html", content_len: int = None) -> str:
    _header = ""
    _header += "HTTP/1.1 "
    _header += response_code
    _header += "\r\n"
    _header += "Server: Cherkasov Simple Web Server\r\n"
    if content_len is not None:
        _header += "Content-Length: "
        _header += str(content_len)
        _header += "\r\n"
    _header += "Connection: close\r\n"
    _header += "Content-Type: "
    _header += content_type
    _header += "\r\n\r\n"
    return _header


addr = ("localhost", 1337)

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

_server.bind(addr)
_server.listen(1)
while True:
    connection, client_address = _server.accept()
    try:
        while True:
            data = connection.recv(1024)
            request = data.decode("utf-8")
            print(request)
            header = create_header("200", "text/html", len(html.encode()))
            connection.send(header.encode())
            connection.send(html.encode())

    finally:
        connection.close()



