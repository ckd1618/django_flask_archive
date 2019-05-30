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
    return render(request, 'firstApp/index1.html' )

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
    # print(result)
    if result:
        request.session['userId'] = user.id
    else:
        messages.error(request, 'Your Email or Password does not match.')
    return redirect('/dashboard')

def dashboard(request):

    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    user = User.objects.get(id=request.session['userId'])
    # print('userId: {}'.format(request.session['userId']))
    info = Job.objects.filter(employee=None)
    
    myjobs = Job.objects.filter(employee=request.session['userId'])
    #This is how to get something out of the classes
    # x=Job.objects.filter(id=10).values()
    # print(x)
    # print(x[0]['title'])
    # print(Job.objects.filter(id=10).values()[0]['title'])
    #The [0] is because the dictionary is the first item in a list, stupid i know.
    context = {
        'user': user,
        'info': info,
        'myjobs' : myjobs,
    }
    
    # request.session['history'].append('/dashboard')
    # request.session.modified = True
    # print(request.session['history'])

    
    return render(request, 'firstApp/dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addjob(request):
    
    # request.session['history'].append('/addjob')
    # request.session.modified = True
    # print(request.session['history'])
    return render(request, 'firstApp/addjob.html' )

def addjobsubmit(request):
    form = request.POST
    errors = []
    user = User.objects.get(id=request.session['userId'])

    if len(form['title']) <4:
        errors.append('Title must be greater than 4 characters long')
    if len(form['desc']) <11:
        errors.append("Title must be greater than 10 characters long")
    if len(form['location']) <1:
        errors.append("Location must not be blank")
    
    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('/addjob')

    else:
        newjob = Job.objects.create(title=form['title'], desc=form['desc'], location=form['location'], user=user)

    return redirect('/dashboard')

def editjobsubmit(request, num5):
    form = request.POST
    errors = []
    user = User.objects.get(id=request.session['userId'])

    if len(form['title']) <4:
        errors.append('Title must be greater than 4 characters long')
    if len(form['desc']) <11:
        errors.append("Title must be greater than 10 characters long")
    if len(form['location']) <1:
        errors.append("Location must not be blank")

    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('/addjob')

    else:
        temp = Job.objects.get(id=num5)
        temp.title=form['title']
        temp.desc =form['desc']
        temp.location=form['location']
        temp.save()

    return redirect('/dashboard')

def editnum(request, num5):
    info = Job.objects.get(id=num5)
    context = {
        'info': info
    }
    
    # request.session['history'].append('/edit/{}'.format(num5))
    # request.session.modified = True
    # print(request.session['history'])
    return render(request, 'firstApp/editnum.html', context)

def viewnum(request, num4):
    info = Job.objects.get(id=num4)
 
    context = {
        'info': info,
    }
    
    # request.session['history'].append('/view/{}'.format(num4))
    # request.session.modified = True
    # print(request.session['history'])
    return render(request, 'firstApp/viewnum.html', context)

def cancel(request, num6):
    Job.objects.get(id=num6).delete()
    return redirect('/dashboard')

# def history(request):
    
#     request.session['history'].pop()
#     request.session.modified = True
#     back = request.session['history'].pop()
#     request.session.modified = True
    # print(request.session['history'])
    return redirect(back)

def addtomyjobs(request, num7):



    #creates a new instance
    # userID = Job.objects.filter(id=num7).values()[0]['user_id']
    # jobdict = Job.objects.filter(id=num7).values()[0]
    # title =jobdict['title']
    # desc = jobdict['desc']
    # location = jobdict['location']
    # user = User.objects.get(id=userID)
    # employee = User.objects.get(id=request.session['userId'])
    # Job.objects.create(title=title, desc=desc, location=location, user=user, employee=employee)
    # Job.objects.get(id=num7).delete()



    #Updates the current instance
    # alteremployee = Job.objects.get(id=num7)
    # alteremployee.employee = User.objects.get(id=request.session['userId'])
    # alteremployee.save()


    alteremployee = Job.objects.get(id=num7)
    alteremployee.employee_id = request.session['userId']
    alteremployee.save()
    # print(alteremployee.__dict__)
    
    return redirect('/dashboard')

    

