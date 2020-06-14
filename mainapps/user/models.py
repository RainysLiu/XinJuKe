from __future__ import absolute_import

from django.db import models

# from house.models import House


class MyUser(models.Model):
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")
    name = models.CharField(verbose_name="用户名", max_length=20)
    upwd = models.CharField(max_length=40)  # 密码
    phone = models.CharField(verbose_name="电话", max_length=20)
    real_name = models.CharField(verbose_name="真实名字", max_length=20)
    id_card = models.CharField(verbose_name="身份证", blank=True, max_length=20)
    cover = models.ImageField(
        verbose_name="用户头像", upload_to="userimg", blank=True,
    )  # 相对于MEDIA_ROOT目录
    email = models.CharField(verbose_name="邮箱", null=True, max_length=20)
    # marked_house = models.ManyToManyField(House,verbose_name='房屋配置',blank=True,)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "t_myuser"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
