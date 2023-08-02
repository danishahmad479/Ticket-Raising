from django.db import models
from django.contrib.auth.models import AbstractUser ,User
from django.conf import settings


# Create your models here.

class Roles(models.Model):
    roles = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) :
        return self.roles


class Department(models.Model):
    department = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.department

class CustomUser(AbstractUser):
    roles = models.ForeignKey(Roles,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    

class Ticket(models.Model):
    CHOICE = (("high","high") , ("medium" ,"medium") , ("low" , "low"))
    title = models.CharField(max_length=200)
    description = models.TextField()
    username = models.ForeignKey(CustomUser,on_delete=models.CASCADE , null = True)
    isapproved =  models.BooleanField(default=False)
    assignedto =  models.ForeignKey(Department,on_delete=models.CASCADE , null = True)
    priority = models.CharField(max_length = 10 , choices = CHOICE)

    def __str__(self):
        return self.title
    
class SendTicketTo(models.Model):
    CHOICE = (("Pending" , "Pending"), ("In Progress" , "In Progress") , ("Completed" , "Completed"))
    CHOICES = (("High" , "High"), ("Medium" , "Medium") , ("Low" , "Low"))
    assigned_to = models.ForeignKey(CustomUser,
                                    on_delete=models.CASCADE , 
                                    limit_choices_to={'is_superuser': False})
    assigned_by = models.ForeignKey(CustomUser,
                                    on_delete= models.CASCADE,
                                    related_name="assigned_tickets" , 
                                    limit_choices_to={'is_superuser': True}, null=True)
    ticket = models.ForeignKey(Ticket , on_delete=models.CASCADE,null= True)
    note =  models.TextField()
    priority = models.CharField(max_length=10 , choices=CHOICES)
    status = models.CharField(max_length=30,choices=CHOICE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.note