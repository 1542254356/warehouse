
from django.contrib import admin


from app.models import UserInfo, Goods, Supplier, WaveHousing, StockOut, Storage, SellOut
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = '欢迎来到小型自选商场管理系统'
    site_title = '小型自选商场管理系统'


admin_site = MyAdminSite(name='myadmin')


admin.site.register(UserInfo)
admin.site.register(Goods)
admin.site.register(Supplier)
admin.site.register(StockOut)
admin.site.register(Storage)
admin.site.register(WaveHousing)
admin.site.register(SellOut)

