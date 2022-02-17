from django.db import models


class ModelFile(models.Model):
    id=models.AutoField(primary_key=True)
    image = models.ImageField('チェック画像',upload_to='documents/')
    # r_image = models.ImageField(upload_to='result/')
    right_lv = models.FloatField('右肩',default=0.0)
    left_lv = models.FloatField(default=0.0)
    theta1 = models.FloatField(default=0.0)
    theta2 = models.FloatField(default=0.0)
    nnbd = models.FloatField(default=0.0)


