from django.contrib import messages

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "imagen": producto.imagen1,
                "nombre": producto.nombre,
                "precio1": producto.precio,
                "acumulado": producto.precio,
                "stock": producto.stock,
                "mensaje": producto.nombre,
                "cantidad": 1,
            }
            self.carrito[id]["mensaje"] = ""
        else:
            if self.carrito[id]["cantidad"] + 1 <= producto.stock:
                self.carrito[id]["cantidad"] += 1
                self.carrito[id]["acumulado"] += producto.precio
            else:
                self.carrito[id]["mensaje"] = "No hay suficiente stock"
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.precio
            self.carrito[id]["mensaje"] = ""
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
