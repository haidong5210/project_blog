from django.db import models
from django.conf import settings
from bs4 import BeautifulSoup
# Create your models here.


class Info(models.Model):
    email = models.EmailField(verbose_name="邮箱")
    nickname = models.CharField(max_length=32, verbose_name="昵称", unique=True)
    tel = models.IntegerField(verbose_name="电话", unique=True, null=True, blank=True)
    avatar = models.FileField(verbose_name="头像", upload_to="avatar", default="/avatar/default.png")
    user = models.OneToOneField(to="User")

    def __str__(self):
        return self.nickname


class User(models.Model):   #settings  ：AUTH_USER_MODEL ="项目名称.UserInfo"
    '''用户信息表'''
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        verbose_name_plural = "用户信息表"

    def __str__(self):
        return self.username


class Article(models.Model):
    '''
    文章表
    '''
    title = models.CharField(max_length=64,verbose_name="文章标题")
    summary = models.CharField(max_length=244, verbose_name="文章概要")
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间",auto_now=True)
    poll_count = models.IntegerField(verbose_name="点赞数",default=0)
    comment_count = models.IntegerField(verbose_name="评论数",default=0)
    read_count = models.IntegerField(verbose_name="阅读数",default=0)

    user = models.ForeignKey(to="User",verbose_name="所属作者",null=True,blank=True)
    classify = models.ForeignKey(to="Classfication",verbose_name="所属类别",null=True,blank=True)
    tags = models.ManyToManyField(to="Tag",through="Article2tag",through_fields=('article', 'tag'),verbose_name="所属标签")
    webartilecla = models.ForeignKey(verbose_name="文章所述主页文章类",to="Web_artile_cla",null=True)

    class Meta:
        verbose_name_plural = "文章表"

    def __str__(self):
        return self.title


class Web_class(models.Model):
    """
    网站分类表
    """
    name = models.CharField(verbose_name="网站分类名",max_length=32)

    def __str__(self):
        return self.name


class Web_artile_cla(models.Model):
    """
    网站文章分类表
    """
    name = models.CharField(max_length=32)
    webclass = models.ForeignKey(verbose_name="网站文章分类名",to="Web_class")

    def __str__(self):
        return self.name


class Article_detail(models.Model):
    '''文章细节表'''
    article = models.OneToOneField(to="Article",verbose_name="所属文章")
    content =models.TextField(verbose_name="文章内容")

    class Meta:
        verbose_name_plural = "文章细节表"

    def __str__(self):
        return self.content


class Tag(models.Model):
    '''标签表'''
    name = models.CharField(max_length=32,verbose_name="标签名")
    blog = models.ForeignKey(to="Blog",verbose_name="所属博客")
    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.name


class Article2tag(models.Model):
    article = models.ForeignKey(verbose_name="文章",to="Article")
    tag = models.ForeignKey(verbose_name="标签",to="Tag")
    class Meta:
        '''联合唯一'''
        unique_together = [
            ("article","tag")
        ]


class Comment(models.Model):
    '''评论表'''
    time = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    content = models.CharField(max_length=265,verbose_name="评论内容")
    up_count = models.IntegerField(default=0)
    user = models.ForeignKey(to="User",verbose_name="评论人",null=True,blank=True)
    article = models.ForeignKey(to="Article",verbose_name="评论文章",null=True,blank=True)
    farther_comment = models.ForeignKey(to="Comment",verbose_name="父级评论",null=True,blank=True)
    # farther_comment = models.ForeignKey("self",verbose_name="父级评论",null=True,blank=True)

    class Meta:
        verbose_name_plural = "评论表"


class Article_poll(models.Model):
    '''文章点赞表'''
    time = models.DateTimeField(verbose_name="点赞时间",auto_now_add=True)
    article = models.ForeignKey(to="Article",verbose_name="点赞文章",null=True,blank=True)   #一个文章可以有多个赞
    user = models.ForeignKey(to="User",verbose_name="点赞人",null=True,blank=True)
    # is_positive = models.BooleanField(default=1,verbose_name="点赞或踩")

    class Meta:
        '''联合唯一'''
        unique_together = ("user", "article",)
        verbose_name_plural = "文章点赞表"


class Comment_poll(models.Model):
    '''评论点赞表'''
    time=models.DateTimeField(verbose_name="点赞时间",auto_now_add=True)
    # is_positive = models.BooleanField(verbose_name="点赞或踩",default=1)
    user = models.ForeignKey(to="User",verbose_name="点赞用户",null=True,blank=True)
    comment = models.ForeignKey(to="Comment",verbose_name="点赞所属评论",null=True,blank=True)   #一个评论可以有多个赞

    class Meta:
        '''联合唯一'''
        unique_together = ("user","comment",)
        verbose_name_plural = "评论点赞表"


class Blog(models.Model):
    '''个人站点表'''
    title = models.CharField(max_length=32,verbose_name="个人博客标题")
    url = models.CharField(max_length=64,verbose_name="路径",unique=True)
    theme = models.CharField(max_length=32,verbose_name="博客主题")
    user = models.OneToOneField(to="User", verbose_name="所属用户")
    class Meta:
        '''通过admin录入数据的时候个中文显示'''
        verbose_name_plural = "个人站点表"

    def __str__(self):
        return self.title


class Classfication(models.Model):
    '''博主个人文章分类表'''
    title = models.CharField(max_length=32, verbose_name="分类标题")
    blog = models.ForeignKey(to="Blog",verbose_name="所属博客")

    class Meta:
        verbose_name_plural = "分类表"

    def __str__(self):
        return self.title



