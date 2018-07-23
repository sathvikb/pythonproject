from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

# Register your models here.
#admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Client)
admin.site.register(models.Order)
def make_stock_available(modeladmin, request, queryset):
    for obj in queryset:
        obj.stock=obj.stock+50
        obj.save()
make_stock_available.short_description = 'Update the stock'
class ProductAdmin(admin.ModelAdmin):
      list_display = ('name','category','price','available','stock')
      actions = [make_stock_available]
admin.site.register(models.Product,ProductAdmin)
