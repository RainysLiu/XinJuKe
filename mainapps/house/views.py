import os
import time

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from house.models import House, Area, Facility, Collections
from order.models import Order
from utils import rank
from user import login_test

# 查询当前相关的其它房子
def relative_houses(house):
    # 查询当前房子相关信息的房子的queryset，存入字典
    relative_houses_list = [
        House.objects.filter(name__contains=house.name[:2]),
        House.objects.filter(region__contains=house.region[:2]),
        House.objects.filter(address__contains=house.address[:2]),
        House.objects.filter(community__contains=house.community[:2]),
    ]
    # 双层遍历该列表，获取相关信息的房屋的id
    relative_houseid_list = []
    for relative_houses in relative_houses_list:
        for relative_house in relative_houses:
            if relative_house:
                relative_houseid_list.append(relative_house.id)
    relative_houseid_list = list(set(relative_houseid_list))
    return relative_houseid_list


def show(request, house_id):
    user_id = request.session.get("user_id")
    house = House.objects.get(pk=house_id)
    relative_houseids = relative_houses(house)
    print("相关的房源：", relative_houseids)
    rank_houses = []
    rank_ids = rank.get_day_rank_ids()  # 查询当日所有的浏览量的数据
    print("rank_ids:" + str(rank_ids))
    for house_tup in rank_ids:
        id = int(house_tup[0].decode())
        count = round(house_tup[1])
        if id in relative_houseids:
            rank_houses.append((House.objects.get(pk=id), count))
            relative_houseids.remove(id)
    if len(relative_houseids):
        for rest_id in relative_houseids:
            rank_houses.append((House.objects.get(pk=rest_id), 0))
    if len(rank_houses):
        rank_houses = rank_houses[:5]
    if Collections.objects.filter(house=house_id):
        info = {"collectionstatus": "取消收藏"}
    else:
        info = {"collectionstatus": "加入收藏"}
    if Order.objects.filter(user_id=user_id, house=house_id):
        infos = {"status": "预约成功"}
    else:
        infos = {"status": "立即预约"}
    imgs = house.houseimage_set.all()
    response = render(request, "house/show.html", locals())
    print("要添加的房间id:%s" % house.id)
    rank.add_day_rank(house.id)  # 将当前浏览房屋id加入redis
    # 记录最近浏览,在用户中心使用
    if request.session.has_key("user_id"):  # 判断是否已经登录
        key = str(request.session.get("user_id"))
        houses_ids = request.session.get(key, "")
        houses_id = house.id  # 将int型转化为str类型
        if houses_ids != "":  # 判断是否有浏览记录,如果有则继续判断
            if houses_ids.count(houses_id) >= 1:  # 如果已经存在,删除掉
                houses_ids.remove(houses_id)
            houses_ids.insert(0, houses_id)  # 添加到第一个
            if len(houses_ids) >= 6:  # 如果超过6个则删除最后一个
                del houses_ids[5]
        else:
            houses_ids = []
            houses_ids.append(houses_id)
        request.session[key] = houses_ids
        print("用户%s浏览了房屋%s" % (key, houses_id))
    return response


def search(request):
    keywd = request.GET.get("keyword")
    print(keywd)
    houses = House.objects.filter(Q(name__contains=keywd) | Q(area__name__contains=keywd)|
                                  Q(area__parent__name__icontains=keywd) | Q(community__contains=keywd) |
                                  Q(region__contains=keywd) | Q(address__contains=keywd))
    # print(houses)

    paginator = Paginator(houses, per_page=9)  # 分页器
    # 获取page参数值
    pager = paginator.page(request.GET.get("page", 1))  # 获取第一页
    citys = Area.objects.filter(parent__isnull=True).all()
    # regions = Area.objects.filter(parent__name='西安市').all()
    return render(request, "index.html", locals())


@login_test.login
def addhouse(request):
    allfacility = Facility.objects.all()
    allhouse = House.objects.all()
    allregion = Area.objects.filter(parent__isnull=False)
    print(addhouse, allfacility, allregion)
    return render(request, "house/addhouse.html", locals())


def add_handle(request):
    userid = request.session.get("user_id")
    post = request.POST
    tit = post.get("title")
    pri = post.get("price")
    housetype = post.get("house_type")
    rentype = post.get("rent_type")
    img = post.get("img")
    flo = post.get("floor")
    com = post.get("community")
    regi = post.get("region")
    addre = post.get("address")
    facili = post.getlist("facility")
    area = post.get("area")
    for info in [
        tit,
        pri,
        housetype,
        rentype,
        img,
        flo,
        com,
        regi,
        addre,
        facili,
        userid,
        area,
    ]:
        print(info, type(info))

    print("*" * 100)
    house = House()
    house.price = int(pri)
    house.name = tit
    house.house_type = housetype
    house.rent_type = rentype
    house.image = img
    house.community = com
    house.region = regi
    house.address = addre
    house.floor = flo + "层"
    house.user_id = userid
    house.area_id = int(area)
    house.save()
    print("*" * 200)
    for fid in facili:
        fac = Facility.objects.get(pk=int(fid))
        print(fac, type(fac))
        house.facility.add(fac)
        house.save()
        print("添加成功")
    print("*" * 100)
    houses_list = House.objects.filter(user_id=userid)
    return render(request, "user/my_publish.html", locals())


@csrf_exempt
def uploadimg(request):
    print(request.FILES)
    uploadFile = request.FILES.get("img")  # 前端上传文件的字段名

    # uploadFile.name  文件名
    # uploadFile.content_type  文件类型 image/jpeg
    # uploadFile.size  文件大小

    # 写入到服务器的用户头像存储的位置中
    photo_dir = os.path.join(settings.BASE_DIR, "static/images/houseimg")

    file_name = str(round(time.time())) + os.path.splitext(uploadFile.name)[-1]
    print(os.path.join(photo_dir, file_name))

    # 将上传的文件按段(缓存块)写入到目标文件中
    with open(os.path.join(photo_dir, file_name), "wb") as f:
        for chunk in uploadFile.chunks():
            f.write(chunk)

    return JsonResponse({"path": "houseimg/%s" % file_name, "code": 20})
