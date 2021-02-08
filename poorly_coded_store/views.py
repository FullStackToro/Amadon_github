from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    product=Product.objects.get(id=request.POST["price"])
    price_from_form = float(product.price)
    total_charge = quantity_from_form * price_from_form
    print("Charging credit card...")

    orders=Order.objects.all()
    request.session['total_historico'] = 0
    request.session['articulos'] = 0
    for order in orders:
        request.session['total_historico'] += round(float(order.total_price),2)
        request.session['articulos'] += round(order.quantity_ordered, 2)
    request.session['total_charge']=total_charge
    print(type(request.session['total_historico']), request.session['total_historico'])
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

    context={
        'total_order': total_charge,
    }
    return redirect('/display')

def display(request):
    context= {
        'total_historico': round(request.session['total_historico'], 2),
        'total_charge': request.session['total_charge'],
        'articulos': request.session['articulos'],
    }
    return render(request, "store/checkout.html", context)





