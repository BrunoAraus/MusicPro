#aqui se realiza el calculo del total a pagar o total de precio de todos los productos

def total_carrito(request):
    total = 0
    if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])
    return {"total_carrito": total}