from django.shortcuts import render, HttpResponse, redirect
from time import localtime, strftime
from django.utils.crypto import get_random_string
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'firstApp/index1.html')

def register(request):
    form = request.POST
    errors = []

    if len(form['name']) < 3:
        errors.append('Name must be 3 at least characters long.')
    if len(form['alias'])<3:
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
        userNew = User.objects.create(name=form['name'], alias=form['alias'], email=form['email'], password=correctHashedPW)
        request.session['userId'] = userNew.id
    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'This email has not been registered.')
        return redirect('/')

    result = bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())
    print(result)
    if result:
        request.session['userId'] = user.id
    else:
        messages.error(request, 'Your Email or Password does not match.')
    return redirect('/books')

def books(request):
    print('books function triggered')
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    print('books function triggered2')
    user = User.objects.get(id=request.session['userId'])

    context = {
        'user': user,
    }
    print('books function triggered3')
    return render(request, 'firstApp/books2.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')