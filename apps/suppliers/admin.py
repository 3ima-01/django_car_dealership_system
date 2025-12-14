from django.contrib import admin

from apps.suppliers.models import discount, sale, stock, supplier

admin.site.register([supplier.Supplier, stock.Stock, discount.Discount, sale.Sale])
