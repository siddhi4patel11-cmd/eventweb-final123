from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length = 255)
    descitem = models.TextField()
    desc = models.TextField() 
    image = models.ImageField(upload_to='uploads') 
    
    def __str__(self):
        return self.name

class sub_category(models.Model):
    name = models.CharField(max_length = 255)
    category  =  models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads')  
    
    def __str__(self):
        return self.name

class Event(models.Model):
    main_title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploade')
    sub_category = models.ForeignKey(sub_category, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value set to 0.00
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_seats = models.IntegerField()
    available_seat = models.IntegerField()
    location = models.TextField()
    description = models.TextField()
    term_conditions = models.TextField()
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    event_created_by = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.main_title

class CustomUser(models.Model):
    BUYER = 'buyer'
    SELLER = 'seller'
    BOTH = 'both'

    USER_TYPE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
        (BOTH, 'Buyer and Seller'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=BUYER,
    )
    choices=[
        ('male', 'Male'), 
        ('female', 'Female'), 
        ('other', 'Other')
    ]
  
    profile_image = models.ImageField(upload_to='upload')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255) 
    gender = models.CharField(max_length=10)
    
    def __str__(self):
        return self.first_name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value set to 0.00


    def __str__(self):
        return f"{self.user.username} - {self.event.title}"







