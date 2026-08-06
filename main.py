import socket
import ssl

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://" , 1)
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        else:
            raise Exception("unsupported protocol")
        if '/' not in url:
            url = url + '/'
        self.host, self.path = url.split("/" , 1)
        self.path = '/' + self.path
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        if ':' in self.host:
            self.host, self.port = self.host.split(':', 1)
            self.port = int(self.port)
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        self.body = content
        s.close()
        return content

    def show(self):
        in_tag = False
        for char in self.body:
            if char == '<':
                in_tag = True
            elif char == '>':
                in_tag = False
            elif not in_tag:
                print(char , end = '')


url = URL("https://kangarroot.github.io/")
url.request()
url.show()
print("one must imagine sisyphus happy")
