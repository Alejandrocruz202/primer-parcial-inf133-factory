from http.server import HTTPServer ,BaseHTTPRequestHandler
import json
class orden_type:
    def __init__(self,client,status,payment,orden_type):
        self.client =client
        self.status=status
        self.paymeny=payment
        self.orden_type = orden_type

class ordenfisica(orden_type):
    def __init__(self,shipping,products):
        super().__init__(orden_type="fisico")
        self.shipping=shipping
        for product in products:
            self.product=[product]

class ordenDigital(orden_type):
    def __init__(self,code,expiration):
        super().__init__(orden_type="digital")
        self.code=code
        self.expiration=expiration

class ordenFactory:
    def create_orden(self, type):
        if type == "fisico":
            return ordenfisica()
        elif type == "digital":
            return ordenDigital()
        else:
            raise ValueError("Tipo de orden no valido")

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class OrdenequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.orden_factory = ordenFactory()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            orden = data.get("orden_type")
            orden_type = self.orden_factory.create_orden(
                orden
            )
            response_data = {"message": orden_type.deliver()}
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, OrdenequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
