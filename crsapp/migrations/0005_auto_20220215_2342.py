# Generated by Django 3.0 on 2022-02-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crsapp', '0004_auto_20220131_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelfile',
            name='image',
            field=models.ImageField(upload_to='documents/', verbose_name='チェック画像'),
        ),
    ]
