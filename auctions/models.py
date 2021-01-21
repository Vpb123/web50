from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    categories=(('Home','Home'),('Mens_Fashion','Mens_Fashion'),('Womens_Fashion','Womens_Fashion'),('Sports', 'Sports'),('Electronics','Electronics'),('Grocery','Grocery'),('Others','Others'))
    title=models.CharField(max_length=64)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    imgURL=models.URLField(blank=True,max_length=200)
    category=models.CharField(choices=categories,blank=True,max_length=20)
    addedTime=models.DateField('date added',auto_now_add=True)
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    ended=models.BooleanField(default=False)
    winner=models.ForeignKey('User',on_delete=models.CASCADE,null=True,blank=True,related_name='winner')
    def __str__(self):
        return self.title 
class Comment(models.Model):
      added_date=models.DateField("date-added",auto_now_add=True)
      entry=models.TextField()
      listing=models.ForeignKey("Listing", on_delete=models.CASCADE)
      user=models.ForeignKey('User',on_delete=models.CASCADE)
      def __str__(self):
          return f'{self.listing} -> {self.user}'
         
class Bid(models.Model):
        added_date=models.DateField('date-added',auto_now_add=True)
        value=models.DecimalField(max_digits=10,decimal_places=2)
        listing=models.ForeignKey("Listing", on_delete=models.CASCADE)
        user=models.ForeignKey('User',on_delete=models.CASCADE)
        def __str__(self):
            return f'{self.listing} -> {self.user}({self.value})'

class Watchlist(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.listing} -> {self.user}"
        
      