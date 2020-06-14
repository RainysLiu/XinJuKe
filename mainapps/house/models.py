from __future__ import absolute_import
from datetime import datetime
import uuid

import os


from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.
from user.models import MyUser


class Area(models.Model):
    name = models.CharField(verbose_name="地区名", max_length=20)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,  # 级联操作
        verbose_name="所属地区",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "t_area"
        verbose_name = "地区"
        verbose_name_plural = verbose_name


class Facility(models.Model):
    name = models.CharField(verbose_name="设施名字", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "t_facility"
        verbose_name = "配置"
        verbose_name_plural = verbose_name


class House(models.Model):
    name = models.CharField(verbose_name="标题", max_length=50)
    price = models.IntegerField(verbose_name="租赁价格")
    house_type = models.CharField(verbose_name="房屋类型", max_length=50)
    rent_type = models.CharField(verbose_name="租赁方式", max_length=50)
    floor = models.CharField(verbose_name="楼层", max_length=20)
    community = models.CharField(
        verbose_name="小区", max_length=20, blank=True, null=True,
    )
    region = models.CharField(verbose_name="区域", max_length=20, blank=True, null=True,)
    address = models.CharField(verbose_name="地址", max_length=20)
    phone = models.CharField(verbose_name="房东电话", max_length=11, blank=True, null=True,)
    image = models.ImageField(
        verbose_name="房屋主图片", blank=True, null=True, upload_to="houseimg"
    )  # 相对于MEDIA_ROOT目录
    facility = models.ManyToManyField(Facility, verbose_name="房屋配置", blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="房东")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="地区")
    add_time = models.DateTimeField(
        auto_now_add=True, verbose_name="添加时间", blank=True, null=True
    )
    house_detail = UEditorField(
        verbose_name="房屋详情",
        blank=True,
        default="",
        width=640,
        height=480,
        imagePath="ueditor/imgs/",
        filePath="ueditor/files/",
        toolbars="full",
    )  # mini, normal, full

    def __str__(self):
        return self.name

    class Meta:
        db_table = "t_house"
        verbose_name = "房屋信息"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]


class HouseImage(models.Model):
    image = models.ImageField(verbose_name="房屋图片", upload_to="houseimgs")
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="房屋")

    def __str__(self):
        return self.house.name + "图片"

    class Meta:
        db_table = "t_houseimage"
        verbose_name = "房屋图片"
        verbose_name_plural = verbose_name


class Collections(models.Model):
    user = models.ForeignKey(
        MyUser, verbose_name="用户", blank=True, related_name="user_house"
    )
    house = models.ForeignKey(
        House, verbose_name="收藏的房屋", blank=True, related_name="house_user"
    )
    add_time = models.DateTimeField(
        auto_now_add=True, verbose_name="收藏时间", blank=True, null=True
    )

    def __str__(self):
        return self.user.name + "收藏了房屋" + self.house.name

    class Meta:
        db_table = "t_user_collections"
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]
