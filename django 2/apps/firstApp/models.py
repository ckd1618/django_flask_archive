from django.db import models

class User(models.Model):
    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

class Quote(models.Model):
    author = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="usersquote", on_delete=models.CASCADE, null=True, blank=True)
    likestotal = models.IntegerField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

class Like(models.Model):
    likeornot = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='userslike', on_delete=models.CASCADE, null=True, blank=True)
    quote = models.ForeignKey(Quote, related_name="quoteslike", on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

# class Job(models.Model):
#     title = models.CharField(max_length=255, null=True, blank=True)
#     desc = models.TextField(null=True, blank=True)
#     location = models.TextField(null=True, blank=True)
#     user = models.ForeignKey(User, related_name="userName", on_delete=models.CASCADE, null=True, blank=True)
#     employee = models.ForeignKey(User, related_name="useremployee", on_delete=models.CASCADE, null=True, blank=True)
#     createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

     # def __repr__(self):
    #     return "title:{},desc:{},location:{},user:{},employee:{},createdAt:{},updatedAt:{}".format(self.title, self.desc, self.location, self.user, self.employee, self.createdAt, self.updatedAt)


