from django.conf.urls import url,include
from django.core.paginator import Paginator

import xadmin as admin
from django.shortcuts import render
from house.models import *

def goindex(request):
    # 查询一级分类
    citys = Area.objects.filter(parent__isnull=True).all()
    # 获取cid分类id
    city_id = int(request.GET.get('cid', 0))
    region_id = int(request.GET.get('rid',0))
    if city_id:
        if region_id:
            regions = Area.objects.filter(parent_id=Area.objects.get(pk=region_id).parent.id).all()
            houses = House.objects.filter(area_id=region_id).all()
        else:
            regions = Area.objects.filter(parent_id=city_id).all()
            houses = House.objects.filter(area__parent_id=city_id).all()
    else:
        regions = Area.objects.filter(parent__name='西安市').all()  #默认区县为西安市区县
        if region_id:
            houses = House.objects.filter(area_id=region_id).all()  #在首页直接点西安市的区县的房源
        else:
            houses = House.objects.filter().all()   #默认首页显示所有最新房源


    paginator = Paginator(houses, per_page=9)  # 分页器

    # 获取page参数值
    pager = paginator.page(request.GET.get('page', 1))  # 获取第一页

    return render(request, 'index.html', locals())



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^house/', include('house.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^order/', include('order.urls')),
    # url(r'^search/', include('haystack.urls')),     #全文检索
    url(r'', goindex),
]

