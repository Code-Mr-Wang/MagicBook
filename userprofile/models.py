from django.db import models
from django.contrib.auth.models import User
# # 引入内置信号
# from django.db.models.signals import post_save
# # 引入信号接收器的装饰器
# from django.dispatch import receiver


# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',verbose_name="用户")
    # 电话号码字段
    phone = models.CharField("电话",max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True,verbose_name="头像")
    # 个人简介
    bio = models.TextField("个人简介",max_length=500, blank=True)
    mod_date = models.DateTimeField('最后确认时间', auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        verbose_name_plural = verbose_name = '个人信息'

    def __str__(self):
        return 'user {}'.format(self.user.username)


# # 信号接收函数，每当新建 User 实例时自动调用
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# # 信号接收函数，每当更新 User 实例时自动调用
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()