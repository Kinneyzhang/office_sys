# Generated by Django 2.2 on 2019-04-23 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20190423_0556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '讨论s帖子', 'verbose_name_plural': '6. 讨论帖子'},
        ),
        migrations.AlterModelTable(
            name='post',
            table='forum_post',
        ),
    ]
