#aqui se realiza el calculo del total a pagar o total de precio de todos los productos
def total_carrito(request):
    total = 0
    total2 = 0
    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += int(value["acumulado"])
        if request.user.is_authenticated:  #aqui se verifica si el usuario está logeado
            total2 = total * 0.8  #aqui se le aplica un descuento del 20% si el usuario está logeado
    return {"total_carrito": total, "total_carrito_descuento": total2}