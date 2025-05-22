from django.contrib import admin

from .models import Product,Category,Size,Brands,Review,SliderItem
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brands)
admin.site.register(Review)

admin.site.register(SliderItem)
