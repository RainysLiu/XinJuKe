import xadmin
from user.models import MyUser


class MyUserAdmin:
    list_display = ["name"]


xadmin.site.register(MyUser, MyUserAdmin)
