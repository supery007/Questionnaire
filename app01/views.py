import json

from django.contrib import auth
from django.shortcuts import render, redirect, HttpResponse

from app01.blogform import *
from app01.geetest import GeetestLib

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

    cls_list=models.ClassList.objects.all()
    questionnaire_list=models.Questionnaire.objects.filter(creator_id=request.session.get('userID'))
    userinfo=models.UserInfo.objects.filter(id=request.session.get('userID')).first()
    print('userinfo:',userinfo)

    return render(request,'index.html',{'cls_list':cls_list,'questionnaire_list':questionnaire_list,'userinfo':userinfo})

def addquestionnaire(request):
    return HttpResponse('...')


def editquestion(request):
    return HttpResponse('...')
