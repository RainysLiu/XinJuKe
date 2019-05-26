import xadmin
from order.models import Order





class OrderAdmin():
    # 列表显示的字段
    list_display = ['user', 'amount']

xadmin.site.register(Order,OrderAdmin,)