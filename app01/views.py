import json

from django.contrib import auth
from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from app01.blogform import *
from app01.geetest import GeetestLib
from django.db.models import F

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def pcajax_validate(request):
    if request.method == "POST":
        login_response = {"is_login": False, "error_msg": None}
        #  验证验证码
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 扩充 验证用户名密码
        if result:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = models.UserInfo.objects.filter(username=username, password=password).first()
            print(user)
            if user:
                login_response["is_login"] = True
                request.session['is_login'] = True
                request.session['userID'] = user.id
                request.session['userName'] = user.username
            else:
                login_response["error_msg"] = "用户名或密码错误"

        else:
            login_response["error_msg"] = "验证码错误"

        return HttpResponse(json.dumps(login_response))

    return HttpResponse("error")


def login(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_response = {"is_login": False, "error_msg": None}
        user = models.UserInfo.objects.filter(username=username, password=password).first()
        if user:
            auth.login(request, user)
            login_response['is_login'] = True
            request.session['is_login'] = True
        else:
            login_response['error_msg'] = "用户名或密码错误"
        import json
        return HttpResponse(json.dumps(login_response))
    return render(request, 'login.html')


def logoff(request):
    request.session.delete('is_login')
    return redirect('/login/')


'''注册账号'''


def reg(request):
    if request.is_ajax():

        form_obj = RegForm(request.POST)
        regResponse = {'user': None, "errorList": None}
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.get('password')
            email = form_obj.cleaned_data.get('email')
            # tel=form.cleaned_data.get('tel')
            nickname = form_obj.cleaned_data.get('nickname')
            avatar_file = request.FILES.get('avatar_file')

            print('注册信息', username, password, email, nickname, avatar_file)

            # create_user django自带的用户注册会对密码进行加密
            if avatar_file:
                user = models.UserInfo.objects.create_user(username=username, password=password, email=email,
                                                           nickname=nickname, avatar=avatar_file)
            else:
                user = models.UserInfo.objects.create_user(username=username, password=password, email=email,
                                                           nickname=nickname, avatar='avatar/default.png')
            regResponse['user'] = user.username
        else:
            regResponse['errorList'] = form_obj.errors

        import json
        return HttpResponse(json.dumps(regResponse))
    form = RegForm()
    return render(request, 'reg.html', {'form': form})


def index(request):
    if not request.session.get('is_login'):
        return redirect('/login/')

    cls_list = models.ClassList.objects.all()
    questionnaire_list = models.Questionnaire.objects.filter(creator_id=request.session.get('userID'))
    userinfo = models.UserInfo.objects.filter(id=request.session.get('userID')).first()

    return render(request, 'index.html',
                  {'cls_list': cls_list, 'questionnaire_list': questionnaire_list, 'userinfo': userinfo})


def addquestionnaire(request):
    response_dict = {'add_msg': False}
    if request.is_ajax():
        title = request.POST.get('title')
        select_val = request.POST.get('select_val')
        user_id = request.session.get('userID')
        questionnaire_obj = models.Questionnaire.objects.create(title=title, cls_id=select_val, creator_id=user_id)

        if questionnaire_obj:
            response_dict['add_msg'] = True
    return HttpResponse(json.dumps(response_dict))


def del_question(q_list, naire_id):
    question_obj = models.Question.objects.filter(naire_id=naire_id)
    question_obj_list = []
    submit_question_list = []
    for question in question_obj:
        question_obj_list.append(question.id)
    for q in q_list:
        if q['pid']:
            submit_question_list.append(int(q['pid']))

    for id in question_obj_list:
        if id not in submit_question_list:
            models.Question.objects.filter(id=id).delete()




def del_options(op_list, options_id, que):
    options_obj = models.Option.objects.filter(qs_id=options_id)
    options_obj_list = []
    submit_options_list = []
    for obj in options_obj:
        options_obj_list.append(obj.id)
    for option in op_list:
        if not option['id']:
            with transaction.atomic():
                models.Option.objects.create(name=option['title'], score=option['val'], qs_id=options_id)
                models.Question.objects.filter(id=int(que['pid'])).update(caption=que['title'], tp=int(que['type']))
        else:
            with transaction.atomic():
                models.Question.objects.filter(id=int(que['pid'])).update(caption=que['title'], tp=int(que['type']))
                models.Option.objects.filter(id=option['id']).update(name=option['title'],score=option['val'])
                submit_options_list.append(int(option['id']))
    for op_obj_id in options_obj_list:
        if op_obj_id not in submit_options_list:
            models.Option.objects.filter(id=op_obj_id).delete()


def editquestion(request):
    if request.is_ajax():
        q_list = json.loads(request.POST.get('plist'))
        naire_id = json.loads(request.POST.get('naire_id'))
        del_question(q_list, naire_id)
        for que in q_list:

            pid = que.get('pid')
            types = que.get('type')
            options = que.get('options')
            title = que.get('title')
            if not pid:
                if types == '2':
                    quest_obj = models.Question.objects.create(caption=title, tp=int(types), naire_id=naire_id)
                    for op in options:
                        quest_obj.option_set.create(name=op['title'], score=op['val'])
                else:
                    models.Question.objects.create(caption=title, tp=int(types), naire_id=naire_id)
            else:
                if types == '2':
                    del_options(que['options'], que['pid'], que)
                else:
                    option_obj = models.Option.objects.filter(qs_id=int(que['pid']))
                    if not option_obj:
                        models.Question.objects.filter(id=int(pid)).update(caption=title, tp=int(types))
                    else:
                        with transaction.atomic():
                            option_obj.delete()
                            models.Question.objects.filter(id=int(pid)).update(caption=title, tp=int(types))
    return HttpResponse('ok')


def delquestion(request):
    response_dict = {'del_msg': False}
    if request.is_ajax():
        qs_id = request.POST.get('qs_id')
        models.Questionnaire.objects.filter(id=qs_id).delete()
        response_dict['del_msg'] = True

    return HttpResponse(json.dumps(response_dict))


from django import forms

from django.forms import widgets


class QuestionForm(forms.Form):
    tp = forms.CharField(
        initial=1,
        error_messages={
            'required': '选项不能为默认值',
        },
        widget=widgets.Select(

            choices=((1, '打分(1~10)'), (2, '单选'), (3, '建议')),
            attrs={'class': "form-control", 'style': "width: 250px"}),
    )

    caption = forms.CharField(
        error_messages={
            'required': '问题内容不能为空',
        },
        widget=widgets.Textarea(
            attrs={'class': "form-control", 'cols': "5", 'rows': "2", 'style': "width: 600px"}),
    )


def question(request, nid):
    que_list = models.Question.objects.filter(naire_id=nid)
    types = {1: '打分(1~10)', 2: '单选', 3: '建议'}
    return render(request, 'que_list.html', {'que_list': que_list, 'types': types, 'naire_id': nid})


def student_login(request):
    obj = models.Student.objects.filter(user='stu05', pwd='stu05').first()
    request.session['student_info'] = {'id': obj.id, 'user': obj.user}
    return HttpResponse('登录成功')

from django.core.exceptions import ValidationError

def func(val):
    if len(val) < 15:
        raise ValidationError('不能少于15字')

def score(request, class_id, naire_id):
    student_id = request.session['student_info']['id']
    student_name = request.session['student_info']['user']


    # 1. 当前登录用户是否是要评论的班级的学生
    st1 = models.Student.objects.filter(id=student_id, cls_id=class_id).count()
    if not st1:
        return HttpResponse('不是该班学生，只能评论自己班级的问卷!')

    # 2. 你是否已经提交过当前问卷答案
    st2 = models.Answer.objects.filter(stu_id=student_id, question__naire_id=naire_id).count()
    if st2:
        return HttpResponse('你已经参与过调查，无法再次进行')

    # 3. 展示当前问卷下的所有问题
    from django.forms import Form
    from django.forms import fields
    from django.forms import widgets
    question_list = models.Question.objects.filter(naire_id=naire_id)
    field_dict = {}
    for que in question_list:
        if que.tp == 1:
            field_dict['val_%s' % que.id] = fields.ChoiceField(
                label=que.caption,
                error_messages={'required': '必填'},
                widget=widgets.RadioSelect,
                choices=[(i, i) for i in range(1, 11)]
            )
        elif que.tp == 2:
            field_dict['option_id_%s' % que.id] = fields.ChoiceField(
                error_messages={
                    'required': '必选',
                },
                label=que.caption,
                widget=widgets.RadioSelect,
                choices=models.Option.objects.filter(
                qs_id=que.id).values_list('id', 'name'))
        else:
            from django.core.exceptions import ValidationError
            field_dict['content_%s' % que.id] = fields.CharField(
                error_messages={
                    'required': '必填',
                },
                label=que.caption, widget=widgets.Textarea, validators=[func, ])

    MyTestForm = type("MyTestForm", (Form,), field_dict)
    if request.method == 'GET':
        form = MyTestForm()
        return render(request, 'score.html', {'question_list': question_list, 'form': form})
    else:
        # 15字验证
        # 不允许为空
        form = MyTestForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # {'x_2': '3', 'x_9': 'sdfasdfasdfasdfasdfasdfasdf', 'x_10': '13'}
            objs = []
            for key,v in form.cleaned_data.items():
                k,qid = key.rsplit('_',1)
                answer_dict = {'stu_id':student_id,'question_id':qid,k:v}
                objs.append(models.Answer(**answer_dict))
            with transaction.atomic():
                models.Answer.objects.bulk_create(objs)
                models.Questionnaire.objects.filter(id=naire_id).update(count_answer=F('count_answer')+1)
            return HttpResponse('感谢您的参与!!!')
    return render(request, 'score.html', {'question_list': question_list, 'form': form})
