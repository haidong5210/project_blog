# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='文章标题')),
                ('summary', models.CharField(max_length=244, verbose_name='文章概要')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('poll_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('read_count', models.IntegerField(default=0, verbose_name='阅读数')),
            ],
            options={
                'verbose_name_plural': '文章表',
            },
        ),
        migrations.CreateModel(
            name='Article2tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='Article_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=400, verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='所属文章')),
            ],
            options={
                'verbose_name_plural': '文章细节表',
            },
        ),
        migrations.CreateModel(
            name='Article_poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='点赞文章')),
            ],
            options={
                'verbose_name_plural': '文章点赞表',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='个人博客标题')),
                ('url', models.CharField(max_length=64, unique=True, verbose_name='路径')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
            ],
            options={
                'verbose_name_plural': '个人站点表',
            },
        ),
        migrations.CreateModel(
            name='Classfication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '分类表',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('content', models.CharField(max_length=265, verbose_name='评论内容')),
                ('up_count', models.IntegerField(default=0)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='评论文章')),
                ('farther_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment', verbose_name='父级评论')),
            ],
            options={
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='Comment_poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment', verbose_name='点赞所属评论')),
            ],
            options={
                'verbose_name_plural': '评论点赞表',
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('nickname', models.CharField(max_length=32, unique=True, verbose_name='昵称')),
                ('tel', models.IntegerField(blank=True, null=True, unique=True, verbose_name='电话')),
                ('avatar', models.FileField(default='/avatar/default.png', upload_to='avatar', verbose_name='头像')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='标签名')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '用户信息表',
            },
        ),
        migrations.CreateModel(
            name='Web_artile_cla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Web_class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='网站分类名')),
            ],
        ),
        migrations.AddField(
            model_name='web_artile_cla',
            name='webclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Web_class', verbose_name='网站文章分类名'),
        ),
        migrations.AddField(
            model_name='info',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.User'),
        ),
        migrations.AddField(
            model_name='comment_poll',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='点赞用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='评论人'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='article_poll',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='点赞人'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='classify',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Classfication', verbose_name='所属类别'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='app01.Article2tag', to='app01.Tag', verbose_name='所属标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='所属作者'),
        ),
        migrations.AddField(
            model_name='article',
            name='webartilecla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Web_artile_cla', verbose_name='文章所述主页文章类'),
        ),
        migrations.AlterUniqueTogether(
            name='comment_poll',
            unique_together=set([('user', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='article_poll',
            unique_together=set([('user', 'article')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
