from django.db import models
import random 
import string
# Create your models here.

def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    if ticket.objects.filter(automatic_generated_ticket_number=key).exists():
        key = key_generator()
    return key

class ticket(models.Model):
    name=models.CharField(max_length=100,null=False)
    phone_no=models.CharField(max_length=20,null=False)
    address=models.CharField(max_length=250)
    automatic_generated_ticket_number=models.CharField(max_length=6,default='')
    email=models.EmailField()
    description=models.TextField()
    notes=models.TextField()
    img=models.ImageField(blank=True,null=True,upload_to='images/')
    REQUIRED_FIELDS=[name,phone_no,description]