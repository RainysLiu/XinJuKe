from __future__ import absolute_import

from datetime import date

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper

from user.models import MyUser
from house.models import House

# Create your models here.


class OrderNumberField(models.CharField):
    def get_db_prep_value(
        self, value, connection: BaseDatabaseWrapper, prepared=False
    ) -> str:
        if not value:  # 避免 更新时 重新生成 单号
            cursor = connection.cursor()

            cursor.execute("select cn from t_order ORDER by id DESC limit 0, 1")
            row = cursor.fetchone()  # 获取查询记录   返回是tuple

            current_date = date.strftime(date.today(), "%Y%m%d")

            if row:  # 空元组是没有记录的
                cn = row[0]
                date_, number = cn[:8], cn[8:]
                if date_ == current_date:
                    number = str(int(number) + 1).rjust(4, "0")
                    return "%s%s" % (date_, number)

            return "%s0001" % current_date

        return value


class Order(models.Model):
    cn = OrderNumberField(max_length=20, verbose_name="订单号", blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="用户")
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="房屋")
    add_time = models.DateTimeField(
        auto_now_add=True, verbose_name="添加时间", blank=True, null=True
    )
    odify_time = models.DateTimeField(
        verbose_name="更新时间", auto_now=True, blank=True, null=True
    )
    days = models.IntegerField(verbose_name="预定天数")
    house_price = models.IntegerField(verbose_name="房屋价格")
    amount = models.IntegerField(verbose_name="订单金额")
    allstatus = (
        ("0", "待支付"),
        ("1", "已支付"),
        ("2", "待评价"),
        ("3", "已拒单"),
        ("4", "已取消"),
    )
    status = models.CharField(max_length=20, choices=allstatus)
    commit = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.name + "订单"

    class Meta:
        db_table = "t_order"
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name
