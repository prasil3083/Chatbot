from django.shortcuts import render , redirect
from django.http import JsonResponse
import google.generativeai as genai

from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from . models import Chat



GOOGLE_API_KEY ='add your gemini key'
genai.configure(api_key = GOOGLE_API_KEY)

def ask_gemini(message):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(message)
    
    # print(response) #just for the debugging

    answer = response._result.candidates[0].content.parts[0].text.strip()
    return answer

    

# Create your views here.
def chatbot(request):
    if request.method =='POST':
        message = request.POST.get('message')
        response = ask_gemini(message)

        chat = Chat(user = request.user, message = message , response = response , created_at = timezone.now)
        chat.save()
        return JsonResponse({'message' : message , 'response' : response })
    return render(request , 'chatbot.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username , password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        
        else:
            error_message = 'Invalid usernaem or Password'
            return render(request , 'login.html' , {'error_message' : error_message})

    else:
        return render (request , 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message = 'Error Creating Account'
                return render (request , 'register.html',{'error_message' : error_message})
        else:
            error_message = "Passwod don't mathch"
            return render (request , 'register.html',{'error_message' : error_message})
    return render (request , 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
