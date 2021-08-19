from django.urls import path

from .views import (create_customer, customer_detail, CustomersList,
                    scaffoldig_detail, ScaffoldingList, OrderList, home)

app_name = 'scaffolding'

urlpatterns = [
    path('customers/', CustomersList.as_view(), name='customers_list'),
    path('customers/<int:customer_id>', customer_detail,
         name='customer_detail'),
    path('scaffoldings/', ScaffoldingList.as_view(), name='scaffolds'),
    path('scaffoldings/<int:id>', scaffoldig_detail, name='scaffoldig'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('create/', create_customer, name='create_customer'),
    path('', home, name='home'),
]
