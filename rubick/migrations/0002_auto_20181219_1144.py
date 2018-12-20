# Generated by Django 2.0.8 on 2018-12-19 03:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rubick', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='starter',
            field=models.ForeignKey(on_delete=True, related_name='topics_starter', to=settings.AUTH_USER_MODEL, verbose_name='发起者'),
        ),
        migrations.AddField(
            model_name='reply',
            name='created_by',
            field=models.ForeignKey(on_delete=True, related_name='reply_created_by', to=settings.AUTH_USER_MODEL, verbose_name='回复者'),
        ),
        migrations.AddField(
            model_name='reply',
            name='post',
            field=models.ForeignKey(on_delete=True, related_name='reply_post', to='rubick.Post', verbose_name='关联回复'),
        ),
        migrations.AddField(
            model_name='reply',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=True, related_name='reply_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=True, related_name='posts_created_by', to=settings.AUTH_USER_MODEL, verbose_name='回复者'),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(on_delete=True, related_name='posts_topic', to='rubick.Topic', verbose_name='关联主题'),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=True, related_name='posts_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
    ]