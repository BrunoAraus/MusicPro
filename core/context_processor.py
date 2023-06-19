#aqui se realiza el calculo del total a pagar o total de precio de todos los productos
import requests

def total_carrito(request):
    total = 0
    total2 = 0

    #API BANCO CENTRAL
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=211737212&pass=kilOfk917B1z&firstdate=2023-06-07&lastdate=2023-12-30&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
    response = requests.get(url)
    response = response.json()
    dolar = response["Series"]["Obs"][0]["value"] #se le asigna el valor "value" a la variable 'dolar'

    if "carrito" in request.session.keys():
        for key, value in request.session["carrito"].items():
            total += int(value["acumulado"])
        if request.user.is_authenticated:  #aqui se verifica si el usuario está logeado
            total2 = total * 0.8  #aqui se le aplica un descuento del 20% si el usuario está logeado

    total_dolar = (total / float(dolar))
    total_dolar_descuento = (total2 / float(dolar))
    dolar = dolar

    return {"total_carrito": total, "total_carrito_descuento": total2, 'total_dolar': total_dolar, 'total_dolar_descuento': total_dolar_descuento, 'dolar': dolar}