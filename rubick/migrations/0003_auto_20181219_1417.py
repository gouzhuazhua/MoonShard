# Generated by Django 2.0.8 on 2018-12-19 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubick', '0002_auto_20181219_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.IntegerField(max_length=32, unique=True, verbose_name='回复编号'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='reply_id',
            field=models.IntegerField(max_length=32, unique=True, verbose_name='级联回复编号'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_id',
            field=models.CharField(max_length=32, unique=True, verbose_name='主题编号'),
        ),
    ]