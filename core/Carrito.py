from django.contrib import messages

#aqui se define la clase carrito y la forma en que se crea nuestro diccionario
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

    # aqui se realiza el metodo ingresar
    def agregar(self, producto):
        id = str(producto.id)
        # verifica si el producto ya existe en el carrito
        if id not in self.carrito.keys():
             # verifica si hay descuento
            if producto.descuento == 0:
                self.carrito[id] = {
                    "producto_id": producto.id,
                    "imagen": producto.imagen1,
                    "nombre": producto.nombre,
                    "precio1": producto.precio,
                    "precio2": producto.preciodescuento,
                    "descuento": producto.descuento,
                    "acumulado": producto.precio,
                    "stock": producto.stock,
                    "mensaje": producto.nombre,
                    "cantidad": 1,
                }
                self.carrito[id]["mensaje"] = ""
                self.carrito[id]["descuento_login"] = ""
                self.guardar_carrito()
            else:
                self.carrito[id] = {
                    "producto_id": producto.id,
                    "imagen": producto.imagen1,
                    "nombre": producto.nombre,
                    "precio1": producto.precio,
                    "precio2": producto.preciodescuento,
                    "descuento": producto.descuento,
                    "acumulado": producto.preciodescuento,
                    "stock": producto.stock,
                    "mensaje": producto.nombre,
                    "descuentio_login": producto.precio,
                    "cantidad": 1,
                }
                self.carrito[id]["mensaje"] = ""
                self.carrito[id]["descuento_login"] = ""

            self.guardar_carrito()
            # en caso de ya existir el producto en el carro solo lo suma
        else:
            if producto.descuento == 0:
                if self.carrito[id]["cantidad"] + 1 <= producto.stock:
                    self.carrito[id]["cantidad"] += 1
                    self.carrito[id]["acumulado"] += producto.precio
                else:
                    self.carrito[id]["mensaje"] = "No hay suficiente stock"
            else:
                if self.carrito[id]["cantidad"] + 1 <= producto.stock:
                    self.carrito[id]["cantidad"] += 1
                    self.carrito[id]["acumulado"] += producto.preciodescuento
                else:
                    self.carrito[id]["mensaje"] = "No hay suficiente stock"
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session.modified = True

    #elimina el producto del carrito
    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
    #aqui se restan productos del carrito en caso de tener varios de 1 mismo tipo
    def restar(self, producto):
        id = str(producto.id)
        # verifica si el producto ya existe en el carrito
        if id in self.carrito.keys():
             # verifica si hay descuento
            if producto.descuento == 0:
                #realiza la eliminacion de 1 cantidad del producto en el carro
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] -= producto.precio
                self.carrito[id]["mensaje"] = ""
                if self.carrito[id]["cantidad"] <= 0:
                    self.eliminar(producto)
                self.guardar_carrito()
            else:
                #realiza la eliminacion de 1 cantidad del producto en el carro
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["acumulado"] -= producto.preciodescuento
                self.carrito[id]["mensaje"] = ""
                if self.carrito[id]["cantidad"] <= 0:
                    self.eliminar(producto)
                self.guardar_carrito()

    #deja el carrito en blanco
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
