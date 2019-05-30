from django.shortcuts import render, HttpResponse, redirect
from time import localtime, strftime
from django.utils.crypto import get_random_string
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    # if not 'history' in request.session:
    #     request.session['history'] = []
    # request.session['history'].append('/')
    # request.session.modified = True
    # try:
    #     request.session['history']
    # except KeyError:
    #     request.session['history'] = []
    return render(request, 'firstApp/index.html')

def register(request):
    form = request.POST
    errors = []

    if len(form['firstName']) < 3:
        errors.append('Name must be 3 at least characters long.')
    if len(form['lastName'])<3:
        errors.append("Alias must be at least 3 characters long.")
    if len(form['password'])<8 or len(form['confirm'])<8:
        errors.append("Password must be at least 8 characters long.")
    if form['password'] != form['confirm']:
        errors.append('Password and password confirmation must match.')
    
    if errors:
        for e in errors:
            messages.error(request, e)

    else:
        hashedPW = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        correctHashedPW = hashedPW.decode('utf-8')
        userNew = User.objects.create(firstName=form['firstName'], lastName=form['lastName'], email=form['email'], password=correctHashedPW)
        request.session['userId'] = userNew.id
    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'This email has not been registered.')
        return redirect('/')

    result = bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())

    if result:
        request.session['userId'] = user.id
    else:
        messages.error(request, 'Your Email or Password does not match.')
    return redirect('/quotes')

def quotes(request):

    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    user = User.objects.get(id=request.session['userId'])
    allquotes = Quote.objects.all()
    
    # info = Job.objects.filter(employee=None)
    
    # myjobs = Job.objects.filter(employee=request.session['userId'])

    context = {
        'user': user,
        'allquotes': allquotes,
    }
    # request.session['history'].append('/quotes')
    # request.session.modified = True

    return render(request, 'firstApp/quotes.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addnewquote(request):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    form = request.POST

    # user = User.objects.get(id=request.session['userId'])
    # allquotes = Quote.objects.all()

    Quote.objects.create(author=form['author'], desc=form['quote'], user_id=request.session['userId'], likestotal = 0)
    # info = Job.objects.filter(employee=None)
    
    # myjobs = Job.objects.filter(employee=request.session['userId'])
    return redirect('/quotes')

def addlike(request, num1):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    form = request.POST
    likedquote = Quote.objects.get(id=num1)
    # Like.objects.create(likeornot=True, user_id=request.session['userId'], quote=likedquote)
    if not Like.objects.filter(user_id=request.session['userId']).filter(quote=likedquote):
    # print (torf.values())
    # if torf[0][likeornot] == False:
        Like.objects.create(likeornot=True, user_id=request.session['userId'], quote=likedquote)
        
        likedquote.likestotal = likedquote.likestotal +1
        likedquote.save()
    
    
        

   
    # x = Like.objects.create(likeornot=True, user_id=request.session['userId'], quote=likedquote)

    return redirect('/quotes')



def usernum(request, num2):

    all = Quote.objects.filter(user_id=num2)
    context= {
        'all': all,
    }

    return render(request, 'firstApp/usernum.html', context)

def myaccountnum(request):
    



    user = User.objects.get(id=request.session['userId'])
    id=request.session['userId']
    context= {
        'info': user,
        'id': id,
    }

    return render(request, 'firstApp/myaccountnum.html', context)

def myaccountform(request):
    form = request.POST

    alter = User.objects.get(id=request.session['userId'])
    alter.firstName = form['firstName']
    alter.lastName = form['lastName']
    alter.email = form['email']
    alter.save()
    return redirect('/myaccount')

def cancel(request, num6):
    x= Quote.objects.get(id=num6)
    x.delete()
    return redirect('/quotes')

def valquote(request):
    form = request.POST
    errors = []

    if len(form['author']) < 4:
        errors.append('Name must be 3 at least characters long.')
    if len(form['quote'])< 10:
        errors.append("Alias must be at least 3 characters long.")
    
    if errors:
        for e in errors:
            messages.error(request, e)
    else:
        Quote.objects.create(author=form['author'], desc=form['quote'], user_id=request.session['userId'], likestotal = 0)
    # user = User.objects.get(id=request.session['userId'])
    # allquotes = Quote.objects.all()

    
    # info = Job.objects.filter(employee=None)
    return redirect('/quotes')