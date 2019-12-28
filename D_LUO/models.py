# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    btitle = models.CharField(max_length=255)
    bauthor = models.CharField(max_length=1023, blank=True, null=True)
    bedition = models.CharField(max_length=1023, blank=True, null=True)
    bformat = models.CharField(max_length=127, blank=True, null=True)
    bpages = models.IntegerField(blank=True, null=True)
    brating = models.FloatField(blank=True, null=True)
    bratcount = models.IntegerField(blank=True, null=True)
    brevcount = models.IntegerField(blank=True, null=True)
    bgenres = models.CharField(max_length=1023, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


class Bookstore(models.Model):
    bsname = models.CharField(max_length=255, blank=True, null=True)
    bstel = models.CharField(max_length=8)
    baddr = models.CharField(max_length=255, blank=True, null=True)
    bosstel = models.CharField(max_length=13, blank=True, null=True)
    bosspasswd = models.CharField(max_length=255, blank=True, null=True)
    staffpasswd = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookstore'


class Customer(models.Model):
    cname = models.CharField(max_length=255, blank=True, null=True)
    ctel = models.CharField(primary_key=True, max_length=11)
    last_active_time = models.DateTimeField()
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'customer'


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    order_time = models.DateTimeField(blank=True, null=True)
    customer_tel = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer_tel')
    order_amount = models.FloatField()
    order_type = models.IntegerField()
    order_closetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_'


class Orderdetail(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'orderdetail'
        unique_together = (('order', 'book'),)


class Purchaseorder(models.Model):
    poid = models.AutoField(primary_key=True)
    porder_time = models.DateTimeField()
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING)
    porder_amount = models.FloatField()
    porder_type = models.IntegerField()
    porder_closetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchaseorder'


class Purchaseorderdetail(models.Model):
    porder = models.ForeignKey(Purchaseorder, models.DO_NOTHING, primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'purchaseorderdetail'


class Stock(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING)
    stock_quantity = models.IntegerField()
    outprice = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stock'


class StockNotsale(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING)
    stock_quantity = models.IntegerField()
    outprice = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stock_notsale'


class Supplier(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=255, blank=True, null=True)
    stel = models.CharField(max_length=8)
    scity = models.CharField(max_length=31, blank=True, null=True)
    sregtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier'

