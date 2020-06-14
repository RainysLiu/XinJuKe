# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-01 02:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
        ("house", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cn",
                    order.models.OrderNumberField(
                        blank=True, max_length=20, null=True, verbose_name="订单号"
                    ),
                ),
                (
                    "add_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="添加时间"
                    ),
                ),
                (
                    "odify_time",
                    models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间"),
                ),
                ("days", models.IntegerField(verbose_name="预定天数")),
                ("house_price", models.IntegerField(verbose_name="房屋价格")),
                ("amount", models.IntegerField(verbose_name="订单金额")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("0", "待支付"),
                            ("1", "已支付"),
                            ("2", "待评价"),
                            ("3", "已拒单"),
                            ("4", "已取消"),
                        ],
                        max_length=20,
                    ),
                ),
                ("commit", models.TextField(blank=True, max_length=200, null=True)),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="house.House",
                        verbose_name="房屋",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.MyUser",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单信息",
                "verbose_name_plural": "订单信息",
                "db_table": "t_order",
            },
        ),
    ]
