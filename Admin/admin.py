from django.contrib import admin
from .models import Category,Product,Customer,Cart,Payment,OrderPlaced,Wishlist
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","category_name")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","pname","price","description","qty",
                    "image","cat")
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode',]

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id', 'razorpay_payment_status','razorpay_payment_id','paid']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

class WishAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']

admin.site.register(OrderPlaced,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Wishlist,WishAdmin)
