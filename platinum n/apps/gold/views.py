from django.shortcuts import render, redirect
from .models import User, ActivityLog
from django.contrib import messages
import bcrypt
import random 
# Create your views here.
def index(request):
    return render(request, 'gold/index.html')

def register(request):
    form = request.POST
    has_errors = False

    length_valid = User.objects.validate_length(request.POST)
    if 'errors' in length_valid:
        for e in length_valid['errors']:
            messages.error(request, e)
        return redirect('/')

    if len(form['password']) < 8:
        has_errors = True
        messages.error(request, 'Password must be at least 8 characters.')
    if not form['password'] == form['password_confirmation']:
        has_errors = True
        messages.error(request, 'Password and password confirmation do not match')

    if has_errors:
        return redirect('/')

    try:
        user = User.objects.get(email=form['email'])
        messages.error(request, 'User with this email exists. Please login.')
        return redirect('/')

    except User.DoesNotExist:
        # The hashed password -- as a binary string 
        hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        normal_hashed_pw = hashed_pw.decode('utf-8')

        user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=normal_hashed_pw)

        messages.success(request, "You succesfully registered. Please login.")
    
    return redirect('/')

def login(request):
    form = request.POST
    try:
        user = User.objects.get(email=form['email'])

    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist please register.')
        return redirect('/')

    password_correct = bcrypt.checkpw(form['password'].encode(), user.password.encode())

    if not password_correct:
        messages.error(request, 'Email/password does not match.')
        return redirect('/')

    else:

        request.session['user_id'] = user.id 

        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')

    user = User.objects.prefetch_related('following').get(id=request.session['user_id'])

    all_players = User.objects.all().order_by('-gold')

    following_activity = ActivityLog.objects.filter(user__in = user.following.all())
    context = {
        'user': user, 
        'all_players': all_players,
        'activity': following_activity
    }

    return render(request, 'gold/dashboard.html', context)

def gamble(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')


    if request.POST['game_type'] == 'farm':
        gold = random.randint(10,20)
    elif request.POST['game_type'] == 'cave':
        gold = random.randint(5,10)
    elif request.POST['game_type'] == 'house':
        gold = random.randint(2,5)
    elif request.POST['game_type'] == 'casino':
        gold = random.randint(-50,50)

    user = User.objects.get(id=request.session['user_id'])
    user.gold += gold
    user.save()

    new_log = ActivityLog()

    if gold > 0:
        new_log.result = 'positive'
        new_log.message = 'You won {} gold. Congratulations!'.format(gold)
    else:
        new_log.result = 'negative'
        new_log.message = 'You lost {} gold. You should probably stop now!'.format(gold)

    new_log.user = user
    new_log.save()

    return redirect('/dashboard')

def show_player(request, player_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')

    user = User.objects.get(id = player_id)
    
    # Get all the activities for this specific player
    activities = ActivityLog.objects.filter(user = user).order_by('-created_at')

    context = {
        'user': user,
        'activities': activities,
    }
    return render(request, 'gold/player.html', context)

def edit(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user': user, 
        'posts': Post.objects.get(user = user)
    }
    return render(request, 'gold/edit.html', context)

def update(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')

    length_valid = User.objects.validate_length(request.POST)
    print(length_valid)
    if 'errors' in length_valid:
        for e in length_valid['errors']:
            messages.error(request, e)
        return redirect('/edit')

    else:
        update = User.objects.update_player(request.session['user_id'], request.POST)
    
    if 'errors' in update:
        for e in update['errors']:
            messages.error(request, e)
        return redirect('/edit')
    else:
        messages.success(request, "Your profile was updated.")

    return redirect('/edit')

def follow(request, player_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login to be able to view this page.')
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    user_to_follow = User.objects.get(id=player_id)

    user.following.add(user_to_follow)

    messages.success(request, 'You are now following {} {}'.format(user_to_follow.first_name, user_to_follow.last_name))
    
    return redirect('/dashboard')
