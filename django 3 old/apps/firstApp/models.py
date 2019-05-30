from django.db import models

class User(models.Model):
    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

class Trip(models.Model):
    user = models.ForeignKey(User, related_name="userstrip", on_delete=models.CASCADE, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    destination = models.TextField(null=True, blank=True)
    datefrom = models.DateTimeField( null=True, blank=True)
    dateto = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)
    joiners = models.ManyToManyField(User,related_name='usersjoiners')
# class Group(models.Model):
#     joiner = models.ForeignKey(User, related_name='joinerstrip', on_delete=models.CASCADE, null=True, blank=True)
#     trip = models.ForeignKey(Trip, related_name="tripstrip", on_delete=models.CASCADE, null=True, blank=True)
#     createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)




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


