from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone

import jwt
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
SECRET_KEY = getattr(settings, 'SECRET_KEY', None)
ALGORITHM = getattr(settings, 'ALGORITHM', None)
# Create your views here.

def index(request):
    return render(request, 'counseling/index.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST['signin__id']
        password = request.POST['signin__pw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.status = 1
            user.save()
            return redirect('counsel')
        else:
            return render(request, 'counseling/index.html')

@login_required
def counsel(request):
    if request.user.role == 2:
        return render(request, 'counseling/chat_counseler.html')
    else:
        return render(request, 'counseling/chat_counselee.html')

def signUp(request):
    data = request.POST
    signUpName = data["signUpName"]
    signUpId = data["signUpId"]
    signUpPw = data["signUpPw"]
    signUpBirthYear = data["signUpBirthYear"]
    signUpBirthMonth = data["signUpBirthMonth"]
    signUpBirthDay = data["signUpBirthDay"]
    data = {
        'id': signUpId,
        'name' : signUpName,
        'pw': signUpPw
    }
    token_ = jwt.encode(data, SECRET_KEY, ALGORITHM)
    token = token_.decode('utf-8')
    context = {
        'email' : signUpId,
        'token' : token
    }
    emailContent = render_to_string('counseling/email.html', context)
    email = EmailMessage("온실 속 돌멩이 인증메일입니다.", emailContent, to = [signUpId])
    email.content_subtype = "html"
    result = email.send()
    return render(request, 'counseling/index.html')

def email_activate(request, token):
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    name = payload['name']
    result = True
    return render(request, 'counseling/mail_success.html', {"mail_success": result, "signName" : name} )