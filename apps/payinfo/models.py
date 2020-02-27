from django.db import models
from shortuuidfield import ShortUUIDField


class PayInfo(models.Model):

    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=200)
    price = models.FloatField()
    path = models.FilePathField()


class PayInfoOrder(models.Model):

    uuid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('PayInfo', on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    istype = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(default=1)
