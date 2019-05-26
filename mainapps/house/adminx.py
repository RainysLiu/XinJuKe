import xadmin
from xadmin import views

from house.models import  House, HouseImage, Facility,  Area,Collections


class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class GlobalSetting():
    site_title = '心居客后台管理'
    site_footer = '西安心居客科技有限公司'

    #公共搜索模型(问题： 一个模型类不显示搜索框)
    #global_search_models = ['*']

    #设置模型图标
    # global_models_icon = {
    #     MyUser: 'glyphicon glyphicon-th-list',
    #     House: 'glyphicon glyphicon-bookmark',
    #     HouseImage: 'glyphicon glyphicon-list-alt'
    # }

    # 设置app模块的图标
    apps_icons = {
        'house': 'glyphicon glyphicon-house'
    }

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)


# Register your models here.

class HouseAdmin():
    # 列表显示的字段
    list_display = ['name', 'price']
    # 设置字段的样式（编辑表单使用的样式）
    style_fields = {
        'house_detail': 'ueditor'
    }

class HouseImageAdmin():
    # 列表显示的字段
    list_display = ['image', 'house']


class AreaAdmin():
    # 列表显示的字段
    list_display = ['name']

class FacilityAdmin():
    # 列表显示的字段
    list_display = ['name']
class CollectionsAdmin():
    list_display = ['user','house']

xadmin.site.register(House,HouseAdmin,)
xadmin.site.register(HouseImage,HouseImageAdmin,)
xadmin.site.register(Area,AreaAdmin,)
xadmin.site.register(Facility,FacilityAdmin,)
xadmin.site.register(Collections,CollectionsAdmin,)



