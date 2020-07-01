import os
import time
from _sha1 import sha1

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from house.models import Collections

from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect

# Create your views here.
from house.models import House
from user.models import MyUser

from user import login_test

from django.core.mail import send_mail

from utils import db_connect


def register(request):
    return render(request, "user/register.html", {"title": "用户注册"})


def register_handle(request):  # 注册
    # 接收用户输入
    post = request.POST
    uname = post.get("user_name")
    upwd = post.get("pwd")
    upwd2 = post.get("cpwd")
    utel = post.get("tel")
    email = post.get("email")
    print(email)
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf-8"))  # 必须指定要加密的字符串的字符编码
    upwd3 = s1.hexdigest()  # 获得加密之后的结果
    # 创建对象,保存到数据库
    user = MyUser()
    user.name = uname
    user.upwd = upwd3
    user.phone = utel
    user.email = email
    user.save()
    print("存入成功")
    """发送邮件"""
    # 组织邮件信息
    subject = "心居客欢迎信息"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = "<h1>欢迎%s成为心居客注册会员,您的账号为：%s,密码为:%s" % (uname, uname, upwd)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    # 注册成功，转到登录界面
    return render(request, "user/login.html", {"title": "用户注册"})


def register_exist(request):
    uname = request.GET.get("uname")
    count = MyUser.objects.filter(name=uname).count()  # count为0或1
    return JsonResponse({"count": count})


def register_tel_exist(request):
    userid = request.session.get("user_id")
    if userid:
        user = MyUser.objects.get(pk=userid)
        utel = request.GET.get("utel")
        if utel != user.phone:
            telcount = MyUser.objects.filter(phone=utel).count()
            print("该号码存在", telcount)
            return JsonResponse({"tcount": telcount})
        else:
            return JsonResponse({"tcount": 0})
    else:
        utel = request.GET.get("utel")
        telcount = MyUser.objects.filter(phone=utel).count()
        print("该号码存在", telcount)
        return JsonResponse({"tcount": telcount})


def login(request):
    uname = request.COOKIES.get("uname", "")  # 获取cookie
    context = {"title": "用户登录", "error_name": 0, "error_pwd": 0, "uname": uname}
    return render(request, "user/login.html", context)


def login_handle(request):
    # 接受请求信息
    post = request.POST
    uname = post.get("username")
    upwd = post.get("pwd")
    jizhu = post.get("jizhu", 0)  # 当jizhu有值时,即jizhu被勾选等于1时,返回的数据为1,否则get返回后面的0

    # 根据用户名查询对象
    users = MyUser.objects.filter(name=uname)
    print(users)
    if len(users) == 0:
        users = MyUser.objects.filter(phone=uname)  # 查询结果为一个列表
    print(users)

    # 判断：如果未查到则说明用户名错误，如果查到则判断密码是否正确，如果密码正确，则返回用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf-8"))
        if s1.hexdigest() == users[0].upwd:
            print("密码正确")
            url = request.COOKIES.get("url", "/")  # 获取登录之前进入的页面,如果没有,则进入首页
            red = HttpResponseRedirect(url)  # 用变量记住,方便设置cookie
            print("密码正确，已经重定向到", url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie("login", users[0].phone)  # 设置cookie保存用户电话号码
                print("密码正确，用户已记住")
            else:
                red.set_cookie("uname", "", max_age=-1)  # max_age指的是过期时间,当为-1时为立刻过期
                print("密码正确，不记住用户")
            request.session["user_id"] = users[0].id  # 把用户id和名字放入session中
            request.session["user_name"] = users[0].name
            request.session["user_cover"] = str(users[0].cover)
            print("密码正确，session设置完成")
            print(red)
            return red
        else:
            # 密码错误
            context = {
                "title": "用户登录",
                "error_name": 0,
                "error_pwd": 1,
                "uname": users[0].name,
                "upwd": upwd,
            }
            return render(request, "user/login.html", context)
    else:
        # 用户不存在
        context = {
            "title": "用户登录",
            "error_name": 1,
            "error_pwd": 0,
        }
        return render(request, "user/login.html", context)


@login_test.login
def logout(request):
    # request.session.flush()     #清空session信息
    # del request.session['user_id']
    # del request.session['user_name']
    # del request.session['user_cover']
    request.session.flush()
    return redirect("/")


@login_test.login
def info(request):
    uid = request.session["user_id"]
    houses_ids1 = request.session.get(str(uid), "")
    houses_list = []
    for house_id in houses_ids1:
        houses_list.append(House.objects.get(id=int(house_id)))
    if len(houses_list) > 5:
        houses_list = houses_list[:5]
    print(houses_list)
    user = MyUser.objects.get(pk=uid)
    idcard = "*" * 14 + user.id_card[-4:]
    return render(request, "user/userinfo.html", locals())


@login_test.login
def marked(request):
    userid = request.session.get("user_id")
    colletions_list = Collections.objects.filter()
    return render(request, "user/usermarked.html", locals())


@login_test.login
def published(request):
    userid = request.session.get("user_id")
    houses_list = House.objects.filter(user_id=userid)
    return render(request, "user/my_publish.html", locals())


@login_test.login
def collection(request, house_id):
    msg = {}
    user_id = request.session.get("user_id")
    if not user_id:
        msg["code"] = 100
        msg["msg"] = "未登录"
    else:
        if Collections.objects.filter(user=user_id, house=house_id):
            house = Collections.objects.get(house=house_id)
            house.delete()
            msg["code"] = 201
            msg["msg"] = "加入收藏"
        else:
            Collections.objects.create(user_id=user_id, house_id=house_id)
            msg["code"] = 200
            msg["msg"] = "取消收藏"
            msg["msg1"] = "收藏成功"

    return JsonResponse(msg)


@login_test.login
def modifyinfo(request):
    uid = request.session.get("user_id")
    user = MyUser.objects.get(pk=uid)
    return render(request, "user/modifyinfo.html", locals())


@csrf_exempt
def upload_userimg(request):
    print(request.FILES)
    uploadFile = request.FILES.get("img")  # 前端上传文件的字段名

    # uploadFile.name  文件名
    # uploadFile.content_type  文件类型 image/jpeg
    # uploadFile.size  文件大小

    # 写入到服务器的用户头像存储的位置中
    photo_dir = os.path.join(settings.BASE_DIR, "static/images/userimg")

    file_name = str(round(time.time())) + os.path.splitext(uploadFile.name)[-1]
    print(os.path.join(photo_dir, file_name))

    # 将上传的文件按段(缓存块)写入到目标文件中
    with open(os.path.join(photo_dir, file_name), "wb") as f:
        for chunk in uploadFile.chunks():
            f.write(chunk)

    return JsonResponse({"path": "userimg/%s" % file_name, "code": 20})


@login_test.login
def modifyinfo_handle(request):
    imagepath = request.POST.get("img")
    tel = request.POST.get("tel")
    email = request.POST.get("email")
    real_name = request.POST.get("real_name")
    idcard = request.POST.get("idcard")
    print(imagepath, tel, email, real_name, idcard)
    # user = MyUser.objects.get(pk=request.session.get("user_id"))
    # print(user)
    # if imagepath:
    #     user.cover = imagepath
    # user.email = email
    # user.real_name = real_name
    # user.id_card = idcard
    # user.save()
    sql = "update t_myuser set cover='%s',email='%s',real_name='%s',id_card='%s' where id=%s" % \
          (imagepath, email, real_name, idcard, request.session.get("user_id"))
    print(sql)
    db_connect.db_excute(sql)
    print("修改成功")
    # user = MyUser.objects.get(pk=request.session.get("user_id"))
    sql = 'select * from t_myuser where id=%s' % request.session.get("user_id")
    user = db_connect.convert_objects(sql)[0]
    request.session["user_cover"] = str(user.cover)  # 重设session图像路径
    request.session["user_name"] = user.name  # 重设session用户名

    return HttpResponseRedirect("/user/info/", locals())
