from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt



def index(request):
    return render(request, 'login_app/index.html')

def register(request):
    form = request.POST
    errors = []

    if len(form['first_name']) < 3:
        errors.append('First name must be at least 3 characters.')
    if len(form['last_name']) < 3:
        errors.append('Last name must be at least 3 characters.')
    if len(form['password']) < 8:
        errors.append('Password must be at least 8 characters.')
    if not form['password'] == form['password_confirmation']:
        errors.append('Password and password confirmation do not match.')

    if errors:
        for e in errors:
            messages.error(request, e)

    else:
        hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')
        print(hashed_pw)
        print(correct_hashed_pw)
        new_user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=correct_hashed_pw)
        request.session['user_id'] = new_user.id
        print(new_user)
    
    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'Your email does not exists. Please register.')
        return redirect('/')
    
    result = bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())
    print(result)
    if result:
        request.session['user_id'] = user.id
    else:
        messages.error(request, 'Email/Password does not match.')

    return redirect('/user/{}'.format(request.session['user_id']))

def show(request, user_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    # if not request.session['user_id'] == user_id:
    #     messages.error(request, 'You do not have access to this page.')
    #     return redirect('/user/{}'.format(request.session['user_id']))

    user = User.objects.get(id=user_id)

    context = {
        'user': user,
    }
    return render(request, 'login_app/show.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def wall(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    messages = Message.objects.all().select_related('user').prefetch_related('messages_comments', 'messages_comments__user')
    # messages = Message.objects.all().prefetch_related('messages_comments', 'user')
    context = {
        'user':User.objects.get(id=request.session['user_id']),
        'messages': messages,
    }
    return render(request, 'login_app/wall.html', context)

def message(request):
    # user = User.objects.get(id=request.session['user_id'])
    Message.objects.create(content=request.POST['content'], user_id =request.session['user_id'])
    return redirect('/wall')

def comment(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        messages.error(request, 'This message no longer exists.')
        return redirect('/wall')

    Comment.objects.create(content = request.POST['content'],user_id =request.session['user_id'], message = message )

    return redirect('/wall')

    # class User(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Message(models.Model):
#     user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Comment(models.Model):
#     message = models.ForeignKey(Message, related_name="messages_comments", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)