import datetime
import socketserver, socket


def create_header(response_code: str, content_type: str = "text/plain", content_len: int = None) -> str:
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


addr = ("85.113.131.151", 1337)

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

_server.bind(addr)
_server.listen(10)
while True:
    connection, client_address = _server.accept()
    try:
        while True:
            data = connection.recv(1024)
            request = data.decode("utf-8")
            print(request)
            header = create_header("200", "text/plain", len(b"hello"))
            connection.send(header.encode())
            connection.send(b"hello")
    except Exception as e:
        print(e)
    finally:
        connection.close()




