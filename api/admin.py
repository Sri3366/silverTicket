from django.contrib import admin

# Register your models here.

from .models import Product, UPIInfo, Batch, Submission

admin.site.register(Product)
admin.site.register(UPIInfo)
admin.site.register(Batch)
admin.site.register(Submission)