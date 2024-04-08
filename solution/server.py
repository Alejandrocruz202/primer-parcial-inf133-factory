from http.server import HTTPServer ,BaseHTTPRequestHandler
import json
class orden_type:
    def __init__(self,orden_type,client,status,payment):
        self.client =client
        self.status=status
        self.paymeny=payment
        self.orden_type = orden_type

class ordenfisica(orden_type):
    def __init__(self,tipo,client,status,payment,shipping,products):
        super().__init__(tipo,client,status,payment)
        self.shipping=shipping
        self.products=products

class ordenDigital(orden_type):
    def __init__(self,tipo,client,status,payment,code,expiration):
        super().__init__(tipo,client,status,payment)
        self.code=code
        self.expiration=expiration

class ordenFactory:
    def create_orden(self, type,client, estatus,payment,shipping,products):
        if type == "fisico":
            return ordenfisica("fisico",client,estatus,payment,shipping,products)
        else:
            raise ValueError("Tipo de orden no valido")
class ordenService():
    def __init__(self, *args, **kwargs):
        self.orden_factory = ordenFactory()
        super().__init__(*args, **kwargs)
    def add(self, data):
        if(data.get("orden_type")=="fisico"):
            orden = data.get("orden_type",None)
            client = data.get("client", None)
            status = data.get("status", None)
            payment = data.get("paymet", None)
            shipping = data.get("shipping", None)
            products = data.get("products",[])
            orden_type = self.orden_factory.create_orden(
                orden,client,status,payment,shipping,products
            )
        return orden_type
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
        self.ordenService=ordenService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            temp=self.ordenService.add(data)
            HTTPDataHandler.handle_response(self, 201,temp)
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
