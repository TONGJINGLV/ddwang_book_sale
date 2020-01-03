from django.contrib import admin
from .models import Book, Bookstore, Customer, Order, Orderdetail
from .models import Purchaseorder, Purchaseorderdetail, Supplier
# Register your models here.


# these models can only be changed by the boss
class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Book information', {'fields': ['author', 'edition', 'format', 'pages', 'genres']}),
        ('Book sale', {'fields': ['price', 'stock', 'on_sale']}),
        ('Book comments', {'fields': ['score', 'score_num', 'comment_num']})
    ]
    list_display = ('title', 'author', 'genres', 'stock', 'on_sale')
    list_filter = ['on_sale']
    search_fields = ['title', 'author']


admin.site.register(Book, BookAdmin)


class BookstoreAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['bsname']}),
        ('Bookstore information', {'fields': ['bstel', 'baddr', 'bosstel']}),
        ('Bookstore management', {'fields': ['bosspasswd', 'staffpasswd']})
    ]
    list_display = ('bsname', 'bstel', 'baddr')
    # list_filter = ['bauthor', 'bedition','brating']
    search_fields = ['bsname']


admin.site.register(Bookstore, BookstoreAdmin)


class SupplierAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['sname']}),
        ('Supplier information', {'fields': ['stel', 'scity']}),
    ]
    list_display = ('sname', 'stel', 'scity')
    list_filter = ['scity']
    search_fields = ['sname']
admin.site.register(Supplier, SupplierAdmin)


# these models can also be changed by transactions
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Customer information', {'fields': ['cname', 'ctel', 'password']}),
        ('Customer management', {'fields': ['last_active_time']})
    ]
    list_display = ('cname', 'ctel', 'last_active_time')
    list_filter = ['last_active_time']
    search_fields = ['cname']


admin.site.register(Customer, CustomerAdmin)


class OrderdetailInline(admin.TabularInline):
    model = Orderdetail
    extra = 3


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['order_time']}),
        ('Customer information', {'fields': ['customer', 'address', 'ctel']}),
        ('Order information', {'fields': ['type', 'sendtime','closetime']})
    ]
    list_display = ('oid', 'order_time', 'customer', 'type', 'the_state_of_order', 'order_amount')
    list_filter = ['order_time', 'type']
    search_fields = ['oid']
    inlines = [OrderdetailInline]


admin.site.register(Order, OrderAdmin)


class PurchaseorderdetailInline(admin.TabularInline):
    model = Purchaseorderdetail
    extra = 3


class PurchaseorderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['porder_time']}),
        ('Supplier information', {'fields': ['supplier']})]
    list_display = ('poid', 'porder_time', 'supplier', 'amount')
    list_filter = ['porder_time']
    search_fields = ['poid']
    inlines = [PurchaseorderdetailInline]


admin.site.register(Purchaseorder, PurchaseorderAdmin)


