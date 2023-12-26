from django.contrib import admin
from .models import Branch, PaymentOption, Demandtype, Demandrate, Customer, Bill, PaymentCus
# Register your models here.

admin.site.register(Branch)
admin.site.register(PaymentOption)
admin.site.register(Demandtype)
admin.site.register(Demandrate)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(PaymentCus)

