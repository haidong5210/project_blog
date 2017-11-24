import json
import os
import re
from django.shortcuts import render,HttpResponse,redirect
from django.forms import Form,fields,widgets
from app01 import models
from django.conf import settings
from django.core.validators import ValidationError
from django.db.models import Count,F
# Create your views here.


class Reg(Form):
    """
    form组件
    """
    email = fields.CharField(label="邮箱",max_length=64,
                                widget=widgets.EmailInput(attrs={"placeholder": "需要通过邮件激活帐户"}),
                             error_messages={"required":"请输入邮箱地址"})
    tel = fields.CharField(label="手机号码",
                                widget=widgets.TextInput(attrs={"placeholder": "激活帐户需要手机短信验证"}),
                           error_messages={"required": "请输入手机号码"})
    username = fields.CharField(label="登录名称",
                                widget=widgets.TextInput(attrs={"placeholder": "登录用户名，不少于4个字符"}),
                                error_messages={"required": "请输入登录用户名"})
    nickname = fields.CharField(label="显示昵称",
                                widget=widgets.TextInput(attrs={"placeholder": "即昵称，不少于2个字符"}),
                                error_messages={"required": "请输入显示名称"})
    password = fields.CharField(label="密码",
                                widget=widgets.PasswordInput(attrs={"placeholder":"至少八位"}),
                                error_messages={"required": "请输入密码"})
    confirmPassword = fields.CharField(label="确认密码",
                                widget=widgets.PasswordInput(attrs={"placeholder":"请输入确认密码"}),
                                error_messages={"required": "请输入密码"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exit = models.Info.objects.filter(email=email).first()
        if is_exit:
            raise ValidationError("邮箱已存在！！")
        if re.match(r"[\w!#\$%&'\*\+\-\/=\^_`{\|}~.]+@([\w-]+\.)+(com|net|cn|org|me|cc|biz)$",email):
            return email
        raise ValidationError("格式不对！！")

    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        is_exit = models.Info.objects.filter(tel=tel)
        if is_exit:
            raise ValidationError("号码已存在")
        elif not tel:
            raise ValidationError("请输入手机号码")
        elif not len(tel)==11:
            print(tel,len(tel))
            raise ValidationError("手机号必须为11位")
        elif not re.match(r"0?(13|14|15|18)[0-9]{9}",tel):
            raise ValidationError("手机号码格式不对！")
        elif len(tel)==11:
            return tel

    def clean_username(self):
        user = self.cleaned_data.get("username")
        if not user:
            raise ValidationError("请输入登录用户名")
        if len(user) < 5:
            raise ValidationError("不少于四个字符！！")
        is_exit = models.User.objects.filter(username=user)
        if is_exit:
            raise ValidationError("该用户已存在")
        return user

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if not nickname:
            raise ValidationError("请输入显示名称")
        if len(nickname) < 3:
            raise ValidationError("不少于两个字符")
        is_exit = models.Info.objects.filter(nickname=nickname)
        if is_exit:
            raise ValidationError("该昵称已存在")
        return nickname

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise ValidationError("请输入密码")
        if len(password)< 9:
            raise ValidationError("不少于八位")
        return password

    def clean(self):
        password = self.cleaned_data.get("password")
        confirmPassword = self.cleaned_data.get("confirmPassword")
        if password == confirmPassword:
            return self.cleaned_data
        else:
            self.add_error("password","两次输入不一致！！")
            self.add_error("confirmPassword","")


def reg(request):
    if request.method == "GET":
        form = Reg()
        return render(request,"reg.html",{"form":form})
    form=Reg(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps(form.errors))
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    email = form.cleaned_data.get("email")
    tel = form.cleaned_data.get("tel")
    nickname = form.cleaned_data.get("nickname")
    avatar = request.FILES.get("avatar")
    userobj = models.User.objects.create(username=username,password=password)
    models.Info.objects.create(email=email,nickname=nickname,tel=tel,user=userobj,avatar=avatar)
    return HttpResponse(json.dumps(False))


def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    user = request.POST.get("name")
    pwd = request.POST.get("password")
    valid = request.POST.get("valid")
    dict = {"is_login":False,"error":None}
    is_exit = models.User.objects.filter(password=pwd,username=user).first()
    if not valid.upper() == request.session.get(settings.VALID).upper():
        dict["error"] = "验证码错误！"
    elif is_exit:
        request.session[settings.USER] = {"name":user,"password":pwd}
        dict["is_login"]=True
    elif not is_exit:
        dict["error"] = "用户名密码不匹配！"
    return HttpResponse(json.dumps(dict))


def index(request,*args,**kwargs):
    if kwargs:
        web_artile_cla_obj = models.Web_artile_cla.objects.filter(name=kwargs["cate"]).first()
        artile = web_artile_cla_obj.article_set.all()
    else:
        artile = models.Article.objects.all()
    web_obj = models.Web_class.objects.all()
    return render(request,"index.html",{"web_obj":web_obj,"artile":artile})


def img(request):
    """
    生成验证码
    :param request:
    :return:
    """
    # path = os.path.join(settings.BASE_DIR, "static", "img.jpg")
    # with open(path, "rb") as f:
    #     data = f.read()
    # 图像识别相关的库PIL
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    import random
    img = Image.new(mode="RGB",size=(200,40),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw = ImageDraw.Draw(img,"RGB")
    font = ImageFont.truetype(font="static/kumo.ttf",size=25)
    list = []
    for i in range(5):
        num = str(random.randint(0,9))
        zimu = chr(random.randint(65,90))
        dzimu = chr(random.randint(97,122))
        content = random.choice([num,zimu,dzimu])
        draw.text([20+i*35,random.randint(5,15)],text=content,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        list.append(content)
    valid = "".join(list)
    request.session[settings.VALID]= valid

    for i in range(100):
        draw.point([random.randint(0,200), random.randint(0,40)], fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    for i in range(8):
        x1 = random.randint(0, 200)
        y1 = random.randint(0, 40)
        x2 = random.randint(0, 200)
        y2 = random.randint(0, 40)

        draw.line((x1, y1, x2, y2), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return HttpResponse(data)


def logout(request):
    request.session.flush()
    return redirect("/login/")


def homeSite(request,username,**kwargs):
    userobj = models.User.objects.filter(username=username).first()
    blog_obj = userobj.blog
    if not userobj:
        return render(request,"error.html")
    articlelist = userobj.article_set.all()
    classify_list = models.Classfication.objects.filter(blog=blog_obj).annotate(num=Count("article__id")).values_list("title","num","id")
    # 利用聚合拿出个数
    tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(num=Count("article__id")).values_list("name","num","id")
    # print(tag_list)
    dates = models.Article.objects.filter(user=userobj).extra(select={"format_time":"strftime('%%Y-%%m',create_time)"}).values_list('format_time').annotate(Count('id'))


    if kwargs:
        if kwargs.get("leibie") == "tag":
            articlelist = models.Article.objects.filter(tags__id=kwargs.get("canshu"),user=userobj)
        elif kwargs.get("leibie") == "category":
            articlelist = models.Article.objects.filter(classify__id=kwargs.get("canshu"),user=userobj)
        elif  kwargs.get("leibie") == "archive":
            year,mouth = kwargs.get('canshu').split("-")
            articlelist = models.Article.objects.filter(create_time__year=year,user=userobj,create_time__month=mouth)
    return render(request,"home.html",{"username":username,"userobj":userobj,"articlelist":articlelist,
                                       "dates":dates,"tag_list":tag_list,"classify_list":classify_list})


def article(request,**kwargs):
    if not kwargs:
        return render(request, "error.html")
    username=kwargs.get("username")
    userobj = models.User.objects.filter(username=username).first()
    blog_obj = userobj.blog
    classify_list = models.Classfication.objects.filter(blog=blog_obj).annotate(num=Count("article__id")).values_list(
        "title", "num", "id")
    tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(num=Count("article__id")).values_list("name", "num",
                                                                                                       "id")
    dates = models.Article.objects.filter(user=userobj).extra(
        select={"format_time": "strftime('%%Y-%%m',create_time)"}).values_list('format_time').annotate(Count('id'))
    nid = kwargs.get("id")
    article_detail = models.Article_detail.objects.filter(article_id=nid).first()
    comment = models.Comment.objects.filter(article_id=nid)
    return render(request,"article.html",{"article_detail":article_detail,
                                          "username":username,"userobj":userobj,
                                          "dates":dates,"tag_list":tag_list,"classify_list":classify_list,"comment":comment})


def poll(request):
    bool = request.GET.get("bool")
    user_name = request.GET.get("user")
    article_id = request.GET.get("article_id")
    article_user=models.User.objects.filter(article__id=article_id).first()
    poll_user_obj = models.User.objects.filter(username=user_name).first()
    poll_num = models.Article.objects.filter(user=article_user, id=article_id).values_list("poll_count")[0][0]
    is_exit = models.Article_poll.objects.filter(user=poll_user_obj,article_id=article_id)
    dict={"is_poll":poll_num,"error":False,"user":True}
    if user_name:
        if bool and not is_exit:
            models.Article_poll.objects.create(article_id=article_id,user=poll_user_obj)
            models.Article.objects.filter(user=article_user, id=article_id).update(poll_count=F("poll_count")+1)
            poll_new_num = models.Article.objects.filter(user=article_user, id=article_id).values_list("poll_count")[0][0]
            dict["is_poll"]=poll_new_num
        else:
            dict["error"]=True
    else:
        dict["user"] =False
    return HttpResponse(json.dumps(dict))


def comment(request):
    user_name = request.GET.get("user")
    article_id = request.GET.get("article_id")
    content=request.GET.get("comment")
    article_user = models.User.objects.filter(article__id=article_id).first()   #作者
    user_obj = models.User.objects.filter(username=user_name).first()     #当前登陆者
    dict = {"bingo":True}
    if content:
        models.Comment.objects.create(content=content,user=user_obj,article_id=article_id)
        models.Article.objects.filter(user=article_user, id=article_id).update(comment_count = F("comment_count")+1)
    else:
        dict["bingo"] = False
    return HttpResponse(json.dumps(dict))