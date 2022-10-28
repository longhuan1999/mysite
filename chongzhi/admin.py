from django.contrib import admin
from .models import Kami, Taocan, Order, Shangpin, APP_POST
# Register your models here.

class KamiAdmin(admin.ModelAdmin):
    list_display = ('kami','taocan','use','add_date','last_save')
    search_fields = ('kami',)
class TaocanAdmin(admin.ModelAdmin):
    list_display = ('taocan','shangpin','alipay_price','wechat_price')
    search_fields = ('taocan',)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','kami','order_name','order_status','qr_price','order_type','beizhu')
    search_fields = ('order_id','kami','order_status','order_type')
class APP_POSTAdmin(admin.ModelAdmin):
    list_display = ('money','encrypt','time','type','title','deviceid')
    search_fields = ('money','type','title')

admin.site.register(Kami,KamiAdmin)
admin.site.register(Taocan,TaocanAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Shangpin)
admin.site.register(APP_POST,APP_POSTAdmin)