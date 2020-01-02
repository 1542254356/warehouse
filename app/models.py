from django.db import models
import django.utils.timezone as timezone

from django.contrib.auth.models import User

# Create your models here.
#员工信息表
class UserInfo(models.Model):
    # related_name  会在request.user.中使用，也就是别名。
    account = models.OneToOneField(to= User, verbose_name='用户名:', null=True, related_name='userinfo', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='姓名:', null=True, blank=False, max_length=10)
    sex_choice = {('男', '男'), ('女', '女'), }
    job_choice = {(u'仓库主管','仓库主管'),(u'普通员工','普通员工'),(u'用户','用户')}
    sex = models.CharField(verbose_name='性别:', null=False, blank=False, max_length=10, choices= sex_choice, default='女')
    job = models.CharField(verbose_name='职位:', null=False, blank=False, max_length=10, choices= job_choice, default= u'普通员工')
    job_num = models.IntegerField(verbose_name='工号:', null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        # 管理界面显示中文
        verbose_name = verbose_name_plural = "员工信息管理"


# 供应商表
class Supplier(models.Model):
    supID = models.IntegerField(verbose_name='供应商编号:', null=True, blank=False)
    sup_name = models.CharField(verbose_name='供应商名称:', null=False, blank=False, max_length=20, default='请输入供应商名称')
    sup_tel = models.IntegerField(verbose_name='供应商电话:', null=True, blank=False,default=0)

    def __str__(self):
        return self.sup_name

    class Meta:
        verbose_name = verbose_name_plural = "供应商管理"


# 货物表/商品表
class Goods(models.Model):
    goods_sup = models.ForeignKey(to=Supplier, null=True, verbose_name='供应商名称', on_delete=models.CASCADE)
    goodsID = models.IntegerField(primary_key=True, verbose_name='货物编号:', null=False, blank=False,default= 200000)
    goods_name = models.CharField(verbose_name='货物名称:', null=False, blank=False, max_length=20, default='请输入货物名称')
    goods_price =  models.FloatField(verbose_name='货物成本:', null=False, blank=False, default= 0)
    # zhangjian add 12.23
    goods_sprice = models.FloatField(verbose_name='货物售价:', null=False, blank=False, default= 0)
    goods_discount = models.FloatField (verbose_name='折扣:', null=False, blank=False, default=0.0)
    # goods_cost =  models.FloatField(verbose_name='总成本:', null=False, blank=False, default= 0)
    # goods_revenue = models.FloatField(verbose_name='总营收:', null=False, blank=False, default=0)
    # good_amount = models.IntegerField(verbose_name='货物数量:', null=False, blank=False, default= 0)
    # goods_max = models.IntegerField(verbose_name='最大库存量:', null=True, blank= False, default= 1000)
    goods_amount = models.IntegerField(verbose_name='在售数量:', null=False, blank=False, default= 0)
    update_date = models.DateTimeField(verbose_name= '更新日期:', null=True,blank=False)

    def __str__(self):
        return self.goods_name

    @property
    def name(self):
        return self.goods_name

    class Meta:
        verbose_name = verbose_name_plural = "商品信息管理"

# 库存状况表
class Storage(models.Model):
    goods_name = models.OneToOneField(to=Goods, verbose_name='货物名称:', related_name='storage', primary_key= True,on_delete= models.CASCADE)
    storage_amount = models.IntegerField(verbose_name='现有库存:', null=True, blank= False, default= 0)
    storage_max = models.IntegerField(verbose_name='最大库存量:', null=True, blank= False, default= 1000)
    create_date = models.DateTimeField(verbose_name= '更新日期:', null=True,blank=False,default=timezone.now)

    def __str__(self):
        return str(self.goods_name.name)

    class Meta:
        verbose_name = verbose_name_plural = "商品库存管理"
# 销售表
class SellOut(models.Model):
    ssid = models.IntegerField(verbose_name='销售编号', null=False,primary_key=True)
    goods_name = models.ForeignKey( to=Goods, related_name='sell_goods', verbose_name='货物名称:',on_delete= models.CASCADE)
    # goods_name = models.OneToOneField( to=Goods, related_name='sell_goods', verbose_name='货物名称:',on_delete= models.CASCADE)
    res_person = models.ForeignKey(to= UserInfo, verbose_name='用户姓名:', on_delete= models.CASCADE)
    out_date = models.DateTimeField (verbose_name='销售时间:', null=False, blank=False,default=timezone.now)
    out_amount = models.IntegerField (verbose_name='销售数量:', null=False, blank=False,default=1)

    def __str__(self):
        return self.goods_name.name

    class Meta:
        verbose_name = verbose_name_plural = "销售管理"

# 入库表
class WaveHousing(models.Model):
    sup_name = models.ForeignKey(to=Supplier, verbose_name='供应商名称:', on_delete= models.CASCADE)
    goods_name = models.ForeignKey(to=Goods, verbose_name='货物名称:', on_delete= models.CASCADE)
    res_person = models.ForeignKey(to= UserInfo, verbose_name='经办人姓名:', on_delete= models.CASCADE)
    in_date = models.DateTimeField(verbose_name= '入库时间', null=False ,blank=False,default=timezone.now)
    in_price = models.FloatField(verbose_name='入库单价:', null=False,blank=False)
    in_amount = models.IntegerField(verbose_name='入库数量:', null=False,blank=False)
    in_ps = models.CharField(verbose_name='备注:', null=True, blank= True, max_length= 100)
    pay_status = models.BooleanField(default=False)

    def __str__(self):
        return self.goods_name.name

    class Meta:
        verbose_name = verbose_name_plural = "入库单管理"


# 出库表
class StockOut(models.Model):
    sup_name = models.ForeignKey(to=Supplier, verbose_name='供应商名称:', on_delete=models.CASCADE)
    goods_name = models.ForeignKey( to=Goods, verbose_name='货物名称:', on_delete= models.CASCADE)
    res_person = models.ForeignKey(to=UserInfo, verbose_name='经办人姓名:', on_delete= models.CASCADE)
    out_date = models.DateTimeField(verbose_name='出库时间:', null=False, blank=False)
    # out_price = models.FloatField(verbose_name='出库单价:', null=False, blank=False) # 去掉这一项
    out_amount = models.IntegerField(verbose_name='出库数量:', null=False, blank=False)
    out_ps = models.CharField(verbose_name='备注:', null=True, blank=True, max_length=500)
    # goods_discount = models.IntegerField(verbose_name='折扣:', null=False, blank=False, default=10)#放到商品属性
    def __str__(self):
        return self.goods_name.name

    class Meta:
        verbose_name = verbose_name_plural = "出库单管理"