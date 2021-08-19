from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Customer, Scaffolding, Order
from .forms import CreateCustomer
from django.urls import reverse


def home(response):
    return render(response, 'orders/base.html', {})
    # return HttpResponse("Testas")


class CustomersList(ListView):
    model = Customer
    template_name = 'orders/customers.html'


class OrderList(ListView):
    model = Order
    template_name = 'orders/orders.html'


def customer_detail(response, customer_id):
    try:
        customer = get_object_or_404(Customer, id=customer_id)
        if response.method == "POST":
            if response.POST.get("save"):
                for order in customer.order_set.all():
                    if response.POST.get("c" + str(order.id)) == "clicked":
                        order.active = True
                    else:
                        order.active = False
                    order.save()
            elif response.POST.get('newOrder'):
                txt = response.POST.get("new")
                if len(txt) > 2:
                    customer.order_set.create(order=txt, active=False)
                else:
                    print("invalid")
    except Customer.DoesNotExist:
        raise Http404

    return render(response, 'orders/customer_detail.html',
                  {"customer": customer})


class ScaffoldingList(ListView):
    model = Scaffolding
    template_name = 'orders/scaffoldings.html'


def scaffoldig_detail(response, id):
    ls = Scaffolding.objects.get(id=id)
    return render(response, 'orders/scaffolding.html', {'ls': ls})


def create_customer(response):
    if response.method == 'POST':
        form = CreateCustomer(response.POST)
        if form.is_valid():
            company_code = form.cleaned_data["company_code"]
            customer = form.cleaned_data["customer"]
            representative = form.cleaned_data["representative"]
            adress = form.cleaned_data["adress"]
            country = form.cleaned_data["country"]
            email = form.cleaned_data["email"]

            t = Customer(company_code=company_code, customer=customer,
                         representative=representative, adress=adress,
                         country=country, email=email)
            t.save()
            return HttpResponseRedirect(reverse('scaffolding:customer_detail',
                                                args=(t.id,)))

    else:
        form = CreateCustomer()
    return render(response, 'orders/create_customer.html', {"form": form})
