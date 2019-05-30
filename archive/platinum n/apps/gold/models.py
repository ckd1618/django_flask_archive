from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def validate_length(self, form_data):
        errors = []
        for key, val in form_data.items():
            if not key == 'csrf_middlewaretoken':
                if len(val) < 3:
                    errors.append('{} is not 3 characters.'.format(key))
            
        if errors:
            return {'errors': errors}
        else:
            return {'success': True}

    def update_player(self, user_id, form_data):
        
        user = User.objects.get(id=user_id)
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.email = form_data['email']

        user.save()

        return {'success': True}


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    gold = models.IntegerField(default=0)
    following = models.ManyToManyField('self', related_name='following_me')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class BananaBoat(models.Manager):
    pass

class ActivityLog(models.Model):
    result = models.CharField(max_length=15)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BananaBoat()