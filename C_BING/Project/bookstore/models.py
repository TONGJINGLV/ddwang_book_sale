# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    order_time = models.DateTimeField(blank=True, null=True)
    customer_tel = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer_tel')
    order_amount = models.FloatField()
    order_type = models.IntegerField()
    order_closetime = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'order_'


class Orderdetail(models.Model):
    order = models.OneToOneField(Order, models.DO_NOTHING, primary_key=True)
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
    porder = models.OneToOneField(Purchaseorder, models.DO_NOTHING, primary_key=True)
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
