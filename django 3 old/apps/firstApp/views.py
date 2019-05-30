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
    return render(request, 'firstApp/index.html' )

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
    return redirect('/travels')

def travels(request):

    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    

    # info = Job.objects.filter(employee=None)
    
    # myjobs = Job.objects.filter(employee=request.session['userId'])

    
    user = User.objects.get(id=request.session['userId'])
    myplans = Trip.objects.filter(user=user)
    presentuserid = request.session['userId']
    alltrips = Trip.objects.all()
    alltripsexclude = Trip.objects.exclude(user_id=request.session['userId']).exclude(joiners=request.session['userId'])
    # othertrips = alltrips.user.exclude(user_id=)

    mytripsnoti = Trip.objects.filter(joiners=user)


    # presentusertrips = alltrips.user_id.filter(id=request.session['userId'])
    myusertrips = Trip.objects.filter(id=request.session['userId'])
    context = {
        # 'presentusertrips': presentusertrips,
        'myplans': myplans,
        'myusertrips' : myusertrips,
        'presentuserid': presentuserid,
        'alltrips': alltrips,
        'user': user,
        'alltrips': alltrips,
        'alltripsexclude':alltripsexclude,
        'mytripsnoti': mytripsnoti
    }

    

    # request.session['history'].append('/travels')
    # request.session.modified = True

    return render(request, 'firstApp/travels.html', context)

def logout(request):

    request.session.clear()
    return redirect('/')

def addtrip(request):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    return render(request, 'firstApp/addtrip.html' )
    

def addjobr(request):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')

    form = request.POST

    errors = []
    try:
        Trip.objects.create(user_id=request.session['userId'], desc=form['desc'], destination=form['destination'], datefrom=form['datefrom'],dateto=form['dateto'])
    except:
        # errors.append("Please put something into your date field(s)")
        messages.error(request, 'Please put something into your date field(s) as well as all fields.')
        return redirect('/addtrip')





    if len(form['destination']) < 1:
        errors.append('Please enter something into destination.')
    if len(form['destination']) < 1:
        errors.append('Please enter something into description.')
    if form['datefrom'] > form['dateto']:
        errors.append("Revise your travel to date so it is after.")
    
    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('/addtrip')
    # else:
    #     Quote.objects.create(author=form['author'], desc=form['quote'], user_id=request.session['userId'], likestotal = 0)
    # user = User.objects.get(id=request.session['userId'])
    # allquotes = Quote.objects.all()

    
    # info = Job.objects.filter(employee=None)



    return redirect('/travels')

    

    

def viewnum(request, num1):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    chosentrip = Trip.objects.get(id=num1)
    alljoiners = chosentrip.joiners.all()
    print(alljoiners.__dict__)

    context = {
        'chosentrip': chosentrip,
        'alljoiners':  alljoiners,
    }

    return render(request, 'firstApp/viewnum.html', context )

def cancelnum(request, num2):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    thetrip = Trip.objects.get(id=num2)
    user = User.objects.get(id=request.session['userId'])
    thetrip.joiners.remove(user)

    return redirect('/travels')

def joinnum(request, num3):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    user = User.objects.get(id=request.session['userId'])
    chosentrip = Trip.objects.get(id=num3)
    chosentrip.joiners.add(user)


    return redirect('/travels')

def deletenum(request, num4):
    if not 'userId' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    thetrip = Trip.objects.get(id=num4)
    thetrip.delete()

    return redirect('/travels')