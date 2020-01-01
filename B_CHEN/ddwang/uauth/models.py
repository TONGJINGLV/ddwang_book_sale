from django.db import models
from django.core.validators import MinValueValidator

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # 书名，不能为空
    author = models.CharField(max_length=1023, blank=True, null=True)  # 作者
    edition = models.CharField(max_length=1023, blank=True, null=True)  # 出版社
    format = models.CharField(max_length=127, blank=True, null=True)  # 版式，hardcover, etc.
    pages = models.IntegerField(blank=True, null=True)  # 页数
    score = models.FloatField('average score', blank=True, null=True)  # 评分
    score_num = models.IntegerField('the number of readers who scored', blank=True, null=True)  # 评分人数
    comment_num = models.IntegerField('the number of readers who comment', blank=True, null=True)  # 评论人数
    genres = models.CharField(max_length=1023, blank=True, null=True)  # 标签，类别
    stock = models.PositiveIntegerField(default=0)  # 库存量，默认初始时为0，如果没有相应进货单无法直接设置为非0
    price = models.FloatField(default=0,
                              validators=[MinValueValidator(0, 'the price should not below zero.')])  # 销售价
    on_sale = models.CharField('on sale or not',
                               max_length=1,
                               choices=[('Y', 'on sale'), ('N', 'not sale')],
                               default='N')  # 是否上架，只能取'Y' OR 'N'，默认值为‘N’

    def clean(self):
        # The stock should be consistent with records in all kinds of orders.
        # 自动运行检查：当前库存量是否与历史进货量和出货量的计算结果相符，否则报错
        # At first the stock could only be zero if there are not any related orders.
        result = 0
        for delta in self.orderdetail_set.all():
            if delta.order.type == 'Y':
                result -= delta.quantity
            elif delta.order.type == 'N' and delta.order.closetime:
                result += delta.quantity
        for delta in self.purchaseorderdetail_set.all():
            result += delta.quantity
        if int(result) != int(self.stock):
            raise ValidationError(_('the stock is not consistent with records in orders.'))

        # the books on sale should have stock above zero
        # 自动运行检查：图书售罄时不能上架
        if self.stock <= 0 and self.on_sale == 'Y':
            raise ValidationError(_('the books which are out of stock cannot be on sale'))

    def __str__(self):
        return self.title


class Bookstore(models.Model):
    bsname = models.CharField('bookstore name', primary_key=True, max_length=255)  # 书店名，不能重名
    bstel = models.CharField('bookstore tel', max_length=8)  # 书店电话号码，非空
    baddr = models.CharField('bookstore address', max_length=255, blank=True, null=True)  # 书店地址
    bosstel = models.CharField('boss tel', max_length=13, blank=True, null=True)  # 店主电话
    bosspasswd = models.CharField('boss password', max_length=255, blank=True, null=True)  # 店主密码
    staffpasswd = models.CharField('staff password', max_length=255, blank=True, null=True)  # 员工密码

    def __str__(self):
        return self.bsname


class Customer(models.Model):
    cname = models.CharField('customer name', primary_key=True, max_length=255)  # 客户名，不能重名
    ctel = models.CharField('customer tel', max_length=11, blank=True, null=True)  # 客户电话
    last_active_time = models.DateTimeField(blank=True, null=True)  # 最后活跃时间
    password = models.CharField('customer password', max_length=255, default='12345678')
    # 密码，若用户自己不设置则默认为‘12345678’
    session = models.TextField(null=True, blank=True)  # 购物车详情

    def __str__(self):
        return self.cname


class Order(models.Model):
    oid = models.AutoField(primary_key=True)  # 订单编号
    order_time = models.DateTimeField()  # cannot be future time， 下单时间
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # 客户，一个客户可对应多个订单，且删除时阻止
    address = models.CharField(max_length=255, blank=True, null=True)  # 地址
    ctel = models.CharField('customer tel', max_length=11, blank=True, null=True)  # 联系电话
    type = models.CharField('buy or return',
                            max_length=1,
                            choices=[('Y', 'buy'), ('N', 'return')],
                            default='Y')  # 订单种类，只能取'Y'（意为购买订单） OR 'N'（意为退货订单），默认值为‘N’
    sendtime = models.DateTimeField('Send Time', blank=True, null=True)  # 书店（购买订单）或客户（退货订单）发货时间
    closetime = models.DateTimeField('Close Time', blank=True, null=True)  # 客户（购买订单）或书店（退货订单）收货时间

    def clean(self):
        # send time must be later than order_time and not future
        if self.sendtime:
            if self.sendtime < self.order_time:
                raise ValidationError(_('send time cannot be earlier than order time'))
        # close time must be later than send time and not future
        if self.closetime and self.sendtime:
            if self.closetime < self.sendtime:
                raise ValidationError(_('close time cannot be earlier than send time'))

    def __str__(self):
        return str(self.oid)

    # to show the state of the order
    def the_state_of_order(self):
        if self.sendtime:
            if self.closetime:
                return 'closed'
            else:
                return 'goods on the way'
        else:
            return 'not delivered yet'

    # to automatically generate the amount of money
    def order_amount(self):
        result = 0
        for orde in self.orderdetail_set.all():
            result += orde.book.price * orde.quantity
        return result

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # change the stock automatically when books are really returned
        # 对于退货订单，只有真正收货时才更新库存
        if self.type == 'N' and self.closetime is not None:
            super().save()
            if self.closetime:
                for record in self.orderdetail_set.all():
                    record.book.stock += record.quantity
                    record.book.save()
        else:
            super().save()


class Orderdetail(models.Model):
    odid = models.AutoField(primary_key=True)  # 订单详情记录编号
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 订单，一个订单对应多个订单详情，删除时级联操作
    book = models.ForeignKey(Book,
                             on_delete=models.PROTECT)  # 书，一种书对应多个订单详情，删除时阻止
    quantity = models.PositiveIntegerField(default=0)  # 书的数量，默认值为0

    def save(self, force_insert=True, force_update=False, using=None,
             update_fields=None):
        # change the stock automatically when orders are created
        # because it means those books has been ordered
        # and can not be ordered by another customer even before delivering
        # 订单提交时就自动修改库存，因为提交就相当于预定了，哪怕还没发货也不能卖给别人了
        # 只能插入新记录不能修改已有记录，以免重复更新库存
        if self.order.type == 'Y':
            delta = self.book.stock - self.quantity
            if delta > 0:
                self.book.stock -= self.quantity
                self.book.save()
            elif delta == 0:
                self.book.stock -= self.quantity
                self.book.on_sale = 'N'
                # when books are out of stock, they were not sale automatically
                self.book.save()
            else:
                raise ValidationError(_('the books are not enough, please choose less or other books'))

        super().save()

    # 不能删除记录，要取消只能再提交一个退货订单
    def delete(self, using=None, keep_parents=False):
        raise ValidationError(_('Sorry, you can not delete existed orders. '
                                'If you want to cancel the order, please submit a "return" order.'
                                'Thank you for your understanding.'))

    class Meta:
        unique_together = (('order', 'book'),)


class Purchaseorder(models.Model):
    poid = models.AutoField(primary_key=True)  # 进货订单号
    porder_time = models.DateTimeField('Order Time')  # 进货时间
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)  # 供应商，一个供应商可以对应多个进货单
    # 删除时阻止操作

    def __str__(self):
        return str(self.poid)

    # to automatically generate the amount of money
    def amount(self):
        result = 0
        for orde in self.purchaseorderdetail_set.all():
            result += orde.price * orde.quantity
        return result


class Purchaseorderdetail(models.Model):
    podid = models.AutoField(primary_key=True)
    purchaseorder = models.ForeignKey(Purchaseorder, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0,
                              validators=[MinValueValidator(0, 'the price should not below zero.')])

    # 进货后自动更新库存，且无法修改，只能插入
    def save(self, force_insert=True, force_update=False, using=None,
             update_fields=None):
        self.book.stock += self.quantity
        self.book.save()
        super().save()

    # 进货记录无法删除
    def delete(self, using=None, keep_parents=False):
        raise ValidationError(_('Sorry, you can not delete existed purchase orders. '))

    class Meta:
        unique_together = (('purchaseorder', 'book'),)


class Supplier(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField('supplier name', max_length=255)
    stel = models.CharField('supplier tel', max_length=8)
    scity = models.CharField('supplier city', max_length=31, blank=True, null=True)

    def __str__(self):
        return self.sname + '_' + self.stel


