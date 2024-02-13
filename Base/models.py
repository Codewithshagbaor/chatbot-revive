# models.py
from django.db import models
import string
import random
from django.contrib.auth.models import User
def generate_random_qid():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(10)) 

class FAQ(models.Model):
    qid = models.CharField(max_length=20, default=generate_random_qid)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Profile(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Offline', 'Offline'),
    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    unique_id = models.CharField(max_length=13, default=str('UID' + ''.join(random.choice(string.digits) for _ in range(10))))
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='user_profile_pics', default=random.choice(['/user_profile_pics/1.jpg', '/user_profile_pics/2.jpg', '/user_profile_pics/3.jpg', '/user_profile_pics/4.jpg', '/user_profile_pics/5.jpg', '/user_profile_pics/6.jpg', '/user_profile_pics/7.jpg', '/user_profile_pics/8.jpg', '/user_profile_pics/9.jpg', '/user_profile_pics/10.jpg', '/user_profile_pics/11.jpg', '/user_profile_pics/12.jpg']))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username
